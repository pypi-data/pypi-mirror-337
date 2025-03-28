import os
from dataclasses import dataclass
from os.path import join, isdir, isfile
from os import scandir
from skimage.measure import regionprops,regionprops_table
from morphonet.data import default_parameters
from morphonet.data.utils import get_previous_cell_in_lineage,get_object_id,indent_xml,list_properties_in_pickle \
    ,get_object_t_id_ch,is_property_a_regionprop,get_all_regionprop_names,get_id_t,get_symetric_cells,get_node
from morphonet.tools import get_longid,get_temp_raw_filename_at, get_temporary_images_prefix,natural_sort,imsave,\
    windows_to_unix_path,get_property_type,connected_neighbors,intensity_offset,intensity_border_variation,roughness,\
    axis_ratio,diameter,convexity,compactness,smoothness
from morphonet.data.dataproperty import DataProperty
import numpy as np
from pathlib import Path
import pickle
import copy
@dataclass
class Image:
    """
    Data structure to hold image metadata and paths for MorphoNet segmentations or intensity images
    """
    channel: int
    time_point: int
    name: str
    original_channel: int
    original_time_point: int
    path: str
    voxel_size: list
    size: list
    encoding: list
    image_temp_path : str
    ndarray : np.ndarray


@dataclass
class AdvancedParameters:
    """
    Data structure of advanced parameters in a dataset.
    Used to keep visualization parameters, and access it using dataset.advanced_parameters.downscale
    """
    seg_downscale: int
    seg_z_downscale: int
    raw_downscale: float
    raw_z_downscale: float
    smoothing: bool
    smoothing_passband: float
    smoothing_iterations: int
    quadratic_clustering: bool
    quadratic_clustering_divisions: int
    decimation: bool
    decimation_reduction: float
    automatic_decimation_threshold: int



class DatasetStep:
    """
    The dataset step is the snapshot of the dataset at a specific round of curation
    Values that are specific to a step : a list of property and a list of segmentation images, the action applied at this step
    """
    def __init__(self, dataset, step , step_folder,action_file):
        self.dataset = dataset
        self.step = step
        self.step_folder = step_folder
        self.properties_by_name = {}
        self.action_file = action_file
        self.segmentations_by_time_channel = {}


    def get_action(self):
        """
        Read the action file of the step, and returns its content (an action file path is given when creating the step)

        :returns: Content of the action file (the step action)
        :rtype: str
        """
        action = ""
        if os.path.isfile(self.action_file):
            f = open(self.action_file,'r')
            action = f.read()
            f.close()
        return action

    def list_cells_in_action(self):
        """
        List the cells found that were updated at the step, found in the action file

        :returns: Cells identifier : time, identifier, channel, label
        :rtype: list
        """
        action = self.get_action()
        found_cells = None
        cell_list = []
        splitted_action = action.split(';')
        for action_param in splitted_action:
            splitted_action_param = action_param.split(':')
            if splitted_action_param[0].strip() == "ID":
                found_cells = splitted_action_param[1].strip()
                break
        if found_cells is not None:
            number_of_separators = 0
            found_cells = found_cells.replace("[","").replace("]","")
            curr_cell = ""
            for char in found_cells:
                if char == "'":
                    number_of_separators += 1
                if number_of_separators < 2:
                    if char != " " and char != "'":
                        if number_of_separators == 1:
                            curr_cell += char
                else:
                    cell_list.append(curr_cell)
                    curr_cell = ""
                    number_of_separators = 0
        return cell_list

    def list_cells_in_action_by_label(self):
        """
        List the cells found that were updated at the step, found in the action file , and group them by their label

        :returns: Cells identifier by label: {label: [t,id,ch, ...]}
        :rtype: dict
        """
        action = self.get_action()
        found_cells = None
        cell_list_by_label = {}
        splitted_action = action.split(';')
        for action_param in splitted_action:
            splitted_action_param = action_param.split(':')
            if splitted_action_param[0].strip() == "ID":
                found_cells = splitted_action_param[1].strip()
                break
        if found_cells is not None:
            number_of_separators = 0
            found_cells = found_cells.replace("[","").replace("]","")
            curr_cell = ""
            for char in found_cells:
                if char == "'":
                    number_of_separators += 1
                if number_of_separators < 2:
                    if char != " " and char != "'":
                        if number_of_separators == 1:
                            curr_cell += char
                else:
                    current_label = 0
                    splitted_cell = curr_cell.split(",")
                    if len(splitted_cell) > 3: # the label is stored in curr_cell
                        current_label = int(splitted_cell[-1])
                    if current_label not in cell_list_by_label:
                        cell_list_by_label[current_label] = []
                    cell_list_by_label[current_label].append(splitted_cell[0]+","+splitted_cell[1]+","+splitted_cell[2])
                    curr_cell = ""
                    number_of_separators = 0
        return cell_list_by_label

    def get_plugin_name(self):
        """
        Return the name of the plugin used during the step, found in the action file

        :returns: Name of the plugin
        :rtype: str
        """
        action = self.get_action()
        splitted_action = action.split(';')
        for action_param in splitted_action:
            splitted_action_param = action_param.split(':')
            if splitted_action_param[0].strip().lower() == "plugin":
                return splitted_action_param[1].strip()
        return None

    def get_plugin_parameters(self):
        """
        Return the parameters of the plugin used during the step, found in the action file

        :returns: Parameters of the plugin
        :rtype: str
        """
        action = self.get_action()
        splitted_action = action.split(';')
        params = []
        for action_param in splitted_action:
            #print(action_param)
            if action_param != '':
                splitted_action_param = action_param.split(':')
                if splitted_action_param[0].strip().lower() not in ["plugin","time","id"]:
                    params.append(action_param.strip())
        return params

    def add_segmentation(self, segmentation_image):
        """
        Add a segmentation image to the dataset step, if not found (search by time + channel)

        :param segmentation_image:
        :type segmentation_image: Image
        """
        if not segmentation_image.time_point in self.segmentations_by_time_channel:
            self.segmentations_by_time_channel[segmentation_image.time_point] = {}
        if not self.contains_segmentation_image_at(segmentation_image.time_point, segmentation_image.channel):
            self.segmentations_by_time_channel[segmentation_image.time_point][segmentation_image.channel] = segmentation_image


    def get_segmentation_at(self, time, channel):
        """
        Return the image at time point and channel given in parameter

        :param time: Time point
        :type time: int
        :param channel: Channel
        :type channel: int
        :return: Image at time point and channel
        :rtype: Image
        """
        if self.contains_segmentation_image_at(time,channel):
            return self.segmentations_by_time_channel[time][channel]
        return

    def clean_property_at(self, time, property_name):
        """
        Remove all values for a specific time point from a property

        :param time: Time point
        :type time: int
        :param property_name: Property name
        :type property_name: str
        """
        if property_name in self.properties_by_name:
            self.properties_by_name[property_name].clean_at(time)


    def contains_property_at(self, time, property_name):
        """
        Test if the current step contains values for a property by name for a given time

        :param time: Time point
        :type time: int
        :param property_name: Property name
        :type property_name: str
        :returns: if contains the property at time given
        :rtype: bool
        """
        prop = self.get_property(property_name)
        if prop is not None:
            return len(prop.get_values_at(time)) > 0
        return False
    def add_property(self, name,path,property_type):
        """
        Add a property to the step, only if not found. If found, return it

        :param name: Property name
        :type name: str
        :param path: Path of the property in the temp folder
        :type path: str
        :param property_type: Type of the property
        :type property_type: str
        :return: The created or found property
        :rtype: DataProperty
        """
        if name in self.properties_by_name:
            return self.properties_by_name[name]
        property_object = DataProperty(self.dataset, name, path, property_type)
        self.properties_by_name[name] = property_object
        return property_object

    def get_property(self, name):
        """
        Retrieve a property object by name

        :param name: Property name
        :type name: str
        :return: Property object or None
        :rtype: DataProperty
        """
        if name in self.properties_by_name:
            return self.properties_by_name[name]
        return None

    def contains_segmentation_image_at(self, time, channel):
        """
        Test if the step contains specific segmentation for time point and channel

        :param time: Time point to find
        :type time: int
        :param channel: Channel to find
        :type channel: int
        :returns: True if step contains a specific segmentation image for time point and channel
        :rtype: bool
        """
        return time in self.segmentations_by_time_channel and channel in self.segmentations_by_time_channel[time] and self.segmentations_by_time_channel[time][channel] is not None




class DatasetAnalysis:
    """
    The dataset is the class that represent a MorphoNet local dataset in temporary files.
    Loading the dataset in memory can be really long
    """
    def __init__(self, name, min_time, max_time, background_value, segmentation_images, raw_images, property_file,
                 creation_date, temp_path, downscale=default_parameters.SEG_DOWNSCALE,
                 z_downscale=default_parameters.SEG_Z_DOWNSCALE, raw_downscale=default_parameters.RAW_DOWNSCALE,
                 raw_z_downscale=default_parameters.RAW_Z_DOWNSCALE, smoothing=default_parameters.APPLY_SMOOTHING,
                 smoothing_passband=default_parameters.SMOOTHING_PASSBAND,
                 smoothing_iterations=default_parameters.SMOOTHING_ITERATIONS,
                 quadratic_clustering=default_parameters.QUADRATIC_CLUSTERING,
                 quadratic_clustering_divisions=default_parameters.QUADRATIC_CLUSTERING_DIVISIONS,
                 decimation=default_parameters.DECIMATION, decimation_reduction=default_parameters.DECIMATION_REDUCTION,
                 automatic_decimation_threshold=default_parameters.AUTOMATIC_DECIMATION_THRESHOLD):
        self.name = name
        self.min_time = min_time
        self.max_time = max_time
        self.background_value = background_value
        self.property_file = property_file
        self.creation_date = creation_date
        self.temp_path = temp_path
        if ":\\" in temp_path and os.name =="posix": #If we find that we are running in windows file system , but linux terminal
            self.temp_path = windows_to_unix_path(temp_path)
            print("updated embryo path to : "+str(self.temp_path))
        self.raw_images = []
        self.advanced_parameters = AdvancedParameters(downscale, z_downscale, raw_downscale, raw_z_downscale, smoothing,
                                                      smoothing_passband, smoothing_iterations, quadratic_clustering,
                                                      quadratic_clustering_divisions, decimation, decimation_reduction,
                                                      automatic_decimation_threshold)
        raw_folder = join(self.temp_path, "raw")
        if isdir(raw_folder):
            for img_obj in raw_images:
                if img_obj is not None:
                    image_path = get_temp_raw_filename_at(raw_folder, img_obj.time_point, self.advanced_parameters.raw_downscale,
                                                          self.advanced_parameters.raw_z_downscale)
                    final_image = img_obj
                    if not isfile(image_path):
                        final_image.image_temp_path = ""
                    else :
                        final_image.image_temp_path = image_path
                    self.raw_images.append(copy.deepcopy(final_image))
        self.properties = {}
        self.steps = {}
        self.list_images_temp = segmentation_images
        self._fill_actions()

    def _get_init_log(self,filename,time=0):
        plug_name = filename
        if "." in filename:
            plug_name = filename.split(".")[0]
        log = "Plugin:" + plug_name + "(External step); Time:"+str(time)+";"
        return log

    def _add_property_to_log(self,step_folder,property_name):
        log_file = join(step_folder, "action")
        if isfile(log_file):
            with open(join(step_folder, "action"), "a") as f:
                f.write(" PR:"+property_name+";")
    def _add_segmentation_to_log(self,step_folder,timepoint,channel):
        log_file = join(step_folder, "action")
        if isfile(log_file):
            with open(join(step_folder, "action"), "a") as f:
                f.write(" SE:"+str(timepoint)+","+str(channel)+";")

    def get_min_time(self):
        """
        Returns the dataset min time point

        :return: min time point
        :rtype: int
        """
        return max(0,self.min_time)

    def get_max_time(self):
        """
        Returns the dataset max time point

        :return: max time point
        :rtype: int
        """
        return max(0,self.max_time)

    def write_segmentation_to_step(self,step, segmentation_array,time,channel,voxel_size=(1,1,1)):
        """ Save a given segmentation to the step folder, and update step action file

        :param step: The step to write in
        :type step: int
        :param segmentation_array: Array of the segmentation image
        :type segmentation_array: ndarray
        :param time: Time point of the segmentation
        :type time: int
        :param channel: Channel of the segmentation
        :type channel: int
        :param voxel_size: Voxel size metadata of the segmentation , optional , default = (1,1,1)
        :type voxel_size: tuple
        """

        if step not in self.steps:
            print("Step not found, not writing anything. Please initialize step before writing in the step")
        path_output = self.steps[step].step_folder
        npz_format = get_temporary_images_prefix(self.temp_path, self.get_number_of_curations()-1,self.min_time)
        if npz_format is None:
            npz_format = self.name+"_t{:01d}_ch{:01d}.npz"
        filename = join(path_output, npz_format.format(time,channel))
        np.savez_compressed(filename, data=segmentation_array, voxel_size=voxel_size)
        self._add_segmentation_to_log(path_output,time,channel)

    def write_property_to_step(self,step, name_file, property_object):
        """ Save a given dictionary to a morphonet text format property. Giving a type to the information is important

        :param step: Step to write in, it has to exist
        :type step: int
        :param name_file: Name of the information and file
        :type name_file: str
        :param property_object: MorphoNet Data property object to save
        :type property_object: MorphNetDataProperty
        """
        if step not in self.steps:
            print("Step not found, not writing anything. Please initialize step before writing in the step")
        path_output = self.steps[step].step_folder
        comments = [name_file,]
        txt = property_object.generate_txt(comments)
        f = open(os.path.join(path_output, property_object.name+".txt"), "w+")
        f.writelines(txt)
        f.close()
        self._add_property_to_log(path_output,property_object.name)
    def initialize_external_step(self, filename):
        """
        Initialize a new step to the dataset TEMP folder, as an external step.

        :param filename: Name of the file that generated a step
        :type filename: str
        :returns: step identifier
        :rtype: int
        """
        step = self.get_number_of_curations() + 1
        step_folder = join(self.temp_path, str(step))
        action_file = join(step_folder, "action")
        self.steps[step] = DatasetStep(self, step,step_folder,action_file)
        if not isdir(step_folder):
            os.makedirs(step_folder)
        command = self._get_init_log(filename)
        if not isfile(action_file):
            with open(action_file, "w") as f:
                f.write(command)
        return step

    def _fill_actions(self):
        steps_folder = [x.name for x in scandir(self.temp_path) if x.is_dir() and x.name.isdigit()]
        sorted_step = natural_sort(steps_folder)
        for step_key in sorted_step:
            action_file = join(self.temp_path, str(step_key), "action")
            step_object = DatasetStep(self,step_key, join(self.temp_path, str(step_key)), action_file)
            self.steps[int(step_key)] = step_object

    def get_action_at(self,step=-1):
        """
        Read the content of the action file for the step given in parameter. If step is -1, returns the action for last step

        :param step: number of the step of curation, if -1 , use the last step
        :type step: int
        :return: action file content or None
        :rtype: str
        """
        real_step = step
        if real_step == -1:
            real_step = self.get_number_of_curations()
        if real_step in self.steps:
            return self.steps[real_step].get_action()
        return None

    def get_cells_updated_at(self,step=-1):
        """
        Read the content of the action file for the step given in parameter, and returns the cell updated.
        If step is -1, returns the action cell list for last step

        :param step: Step of curation, if -1, use the last step
        :type step: int
        :return: list of cell ids content or None
        :rtype: list of str
        """
        real_step = step
        if real_step == -1:
            real_step = self.get_number_of_curations()
        if real_step in self.steps:
            return self.steps[real_step].list_cells_in_action()

    def get_cells_updated_by_selection_at(self,step=-1):
        """
        Read the content of the action file for the step given in parameter, and returns the cell updated, grouping
        them by selection.
        If step is -1, returns the action cell list for last step

        :param step: number of the step of curation, if -1 , use the last step
        :type step: int
        :return: dict of cell ids content by selection or None
        :rtype: dict
        """
        real_step = step
        if real_step == -1:
            real_step = self.get_number_of_curations()
        if real_step in self.steps:
            return self.steps[real_step].list_cells_in_action_by_label()
    def get_plugin_name_at(self,step=-1):
        """
         Read the plugin from the action file for the step given in parameter. If step is -1, returns the action for last step

         :param step: number of the step of curation, if -1 , use the last step
         :type step: int
         :return: plugin found in action file content or None
         :rtype: str
         """
        real_step = step
        if real_step == -1:
            real_step = self.get_number_of_curations()
        if real_step in self.steps:
            return self.steps[real_step].get_plugin_name()


    def get_plugin_parameters_at(self,step=-1):
        """
        Read the plugin from the action file for the step given in parameter. If step is -1, returns the action for last step

        :param step: number of the step of curation, if -1 , use the last step
        :type step: int
        :return: plugin found in action file content or None
        :rtype: str
        """
        real_step = step
        if real_step == -1:
            real_step = self.get_number_of_curations()
        if real_step in self.steps:
            return self.steps[real_step].get_plugin_parameters()

    def export_image(self, time, channel, image_path,step=-1):
        """
        Extract the segmentation image found at given step , channel and time, and save it to image path

        :param channel: Channel in the segmentation
        :type channel: int
        :param time: Time in the segmentation
        :type time: int
        :param image_path: Path where the image should be stored
        :type image_path: str
        :param step: Step to export the dataset from
        :type step: int
        """
        img_step = step
        if img_step == -1:
            img_step = self.get_segmentation_last_step(time, ch=channel)
        img = self.get_segmentation(time,img_step,channel)
        if img is not None and img.ndarray is not None:
            voxel_size = (1, 1, 1)
            if img.voxel_size is not None and len(img.voxel_size) > 0:
                voxel_size = img.voxel_size
            imsave(image_path, img.ndarray, voxel_size=voxel_size)
            del img.ndarray
        else:
            print("Segmentation image not found at time point : " + str(time) + " channel : " + str(channel))
    def export_properties_as_xml(self,output_file,step=-1):
        """
        Export all properties from the dataset as a XML file

        :param output_file: Property file that will be generated
        :type output_file: str
        :param step: Step to export the dataset from, -1 for last step
        :type step: int
        """
        import xml.etree.ElementTree as ET
        f = open(output_file, "w+")
        f.close()
        root = ET.Element('data')
        tree = ET.ElementTree(root)
        tree.write(output_file)

        min_time = self.min_time
        max_time = self.max_time

        source = open(output_file)
        tree = ET.parse(source)
        tree = tree.getroot()
        properties = self.get_all_properties(step)
        for property_object in properties:
            property_object.generate_xml(tree)
        indent_xml(tree)
        mydata = ET.tostring(tree, encoding='utf8', method='xml').decode("utf8")
        myfile = open(output_file, "w+")
        myfile.write(mydata)
        myfile.close()

    def export_properties_as_txt(self, output_folder, include_scikit=True, step=-1):
        """
        Export all properties from the dataset as text files

        :param output_folder: Folder where property texts will be generated
        :type output_folder: str
        :param include_scikit: Whether to include scikit-image or not
        :type include_scikit: bool
        :param step: Step to export the dataset from, -1 for last step
        :type step: int
        """
        properties = self.get_all_properties(step, include_scikit=include_scikit)
        for property_object in properties:
            txt = property_object.generate_txt()
            f = open(os.path.join(output_folder, property_object.name + ".txt"), "w+")
            f.writelines(txt)
            f.close()
    def export_dataset_at_step(self,channel,image_name_template,segmentation_folder_output,step=-1):
        """
        Export all segmentations of the dataset at step (if -1, last step found), into a folder with a specific format

        :param channel: Channel in the segmentation
        :type channel: int
        :param image_name_template: Template image name (with time point formated as %03d or {:03d}
        :type image_name_template: str
        :param segmentation_folder_output: Folder where the segmentation images will be exported
        :type segmentation_folder_output: str
        :param step: Step to export the dataset from
        :type step: int
        """
        for time_point in range(self.min_time, self.max_time + 1):
            if "%" in image_name_template:
                output_image = os.path.join(segmentation_folder_output, (image_name_template % time_point))
            else:
                output_image = os.path.join(segmentation_folder_output,image_name_template.format(time_point))
            self.export_image(time_point,channel,output_image,step)


    def has_intensities_images_at(self,t,channel):
        """
        Determine if dataset has any intensity images for specific t and channel

        :param t: time point
        :type t: int
        :param channel: channel
        :type channel: int
        :return: True if dataset has any intensity images
        :rtype: bool
        """
        img = [x for x in self.raw_images if x.channel == channel and x.time_point == t]
        return len(img) > 0


    def get_intensity_image(self, t, channel,search_for_compressed=False,load_array=True):
        """
        Filter the intensitiy images list to retrieve the intensity image corresponding to time point and channel

        :param t: Time point
        :type t: int
        :param channel: channel
        :type channel: int
        :param search_for_compressed: Whether to search for compressed intensity images instead of normal
        :type search_for_compressed: bool
        :param load_array: Whether to load the intensity images numpy array
        :type load_array: bool
        :return: intensity image corresponding to time point and channel
        :rtype: Image
        """
        from morphonet.tools import imread
        if not self.has_intensities_images_at(t,channel):
            print("No intensities images found for time and channel provided")
            return None
        img = [x for x in self.raw_images if x.channel == channel and x.time_point == t]
        if len(img) == 0:
            return None
        found_image = img[0]
        if load_array:
            path = found_image.path
            if not os.path.exists(path) and search_for_compressed:
                path = found_image.path+".gz"
            if os.path.exists(path):
                array = imread(found_image.path)
                if array is not None:
                    if len(array.shape) == 4:
                        array = array[:,:,:,0]
                    elif len(array.shape) == 5:
                        array = array[:, :, :, 0,0]
                    found_image.ndarray = array
        return found_image

    def get_number_of_curations(self):
        """
        Read the temp folders of the dataset, and count the number of steps

        :return: Number of curation steps
        :rtype: int
        """
        return max(0,len([x.name for x in scandir(self.temp_path) if x.is_dir() and x.name.isdigit()]) - 1)


    def get_segmentation_last_step(self, t, ch=0):
        """
        Returns the last step where a segmentation (found by channel, time) has been updated

        :param t: Time point
        :type t: int
        :param ch: Channel
        :type ch: int
        :return: Last step
        :rtype: int
        """
        max_step = self.get_number_of_curations()
        for step in reversed(range(0, max_step + 1)):
            path = Path(join(self.temp_path, str(step)))
            if path.exists():
                globstr = path.glob("*.npz")
                for result in sorted(globstr, key=lambda item: len(str(item))):
                    image_name = result.name
                    chi = -1
                    ti = -1
                    if "_t" in image_name:
                        if "_ch" in image_name:
                            ti = int(image_name.split("_t")[-1].split("_ch")[0])
                            chi = int(image_name.split("_ch")[-1].split(".")[0])
                        else:
                            ti = int(image_name.split("_t")[-1].split(".")[0])
                            chi = 0
                    if chi > -1 and t > -1:
                        if chi == ch and ti == t:
                            return step
        return 0
    def find_segmentation_path_at_step(self, current_step, t,ch=0):
        """
        Returns the path to the last updated segmentation temporary file for a given time , channel
        (search will be done from given step to 0 , returning the first found)

        :param t: Time point
        :type t: int
        :param ch: Channel
        :type ch: int
        :param current_step: Current step
        :type current_step: int
        :return: Path to the last updated segmentation temporary file
        :rtype: str
        """
        #print("TEST "+str(current_step))
        for step in reversed(range(0, current_step + 1)):
            path = Path(join(self.temp_path, str(step)))
            #print(join(self.temp_path, str(step)))
            if path.exists():
                globstr = path.glob("*.npz")
                for result in sorted(globstr, key=lambda item: len(str(item))):
                    #print(result.name)
                    image_name = result.name
                    chi = -1
                    ti = -1
                    if "_t" in image_name:
                        if "_ch" in image_name:
                            ti = int(image_name.split("_t")[-1].split("_ch")[0])
                            chi = int(image_name.split("_ch")[-1].split(".")[0])
                        else:
                            ti = int(image_name.split("_t")[-1].split(".")[0])
                            chi = 0
                    if chi > -1 and t > -1:
                        if chi == ch and ti == t:
                            return join(self.temp_path, str(step), result.name)
        return None

    def get_scikit_property_last_step(self,name,time=-1):
        """
        Retrieve the last step containing the property given by name.
        Time can be added, if time is not specified, returns the last step found for the curation name. If specified,
        will find the last step for a scikit property at given time

        :param name: property name
        :type name: str
        :param scikit_time: time point, for scikit properties
        :type scikit_time: int
        :return:  the step value
        :rtype: int
        """
        max_step = self.get_number_of_curations()
        for step in reversed(range(0,max_step+1)):
            path = Path(join(self.temp_path, str(step)))
            if path.exists():
                # SCIKIT properties
                globpkl = path.glob("*.regions.pickle")
                for result in sorted(globpkl, key=lambda item: len(str(item))):
                    region_file = join(self.temp_path, str(step), result.name)
                    if time == -1:
                        with open(region_file, "rb") as infile:
                            prop = pickle.load(infile)
                            for cell_id in prop:
                                for property_name in prop[cell_id]:
                                    if property_name == name:
                                        return step
                    else:
                        timep = -1
                        if "_t" in result.name:
                            if "_ch" in result.name:
                                timep = int(result.name.split("_t")[-1].split("_ch")[0])
                                chp = int(result.name.split("_ch")[-1].split(".")[0])
                            else:
                                timep = int(result.name.split("_t")[-1].split(".")[0])
                                chp = 0
                        if timep != -1 and time == timep:
                            with open(region_file, "rb") as infile:
                                prop = pickle.load(infile)
                                for cell_id in prop:
                                    for property_name in prop[cell_id]:
                                        if property_name == name:
                                            return step
        return 0

    def get_property_last_step(self, name, scikit_time=-1):
        """
        Retrieve the last step containing the property given by name.
        Time can be added, if time is not specified, returns the last step found for the curation name. If specified,
        will find the last step for a scikit property at given time

        :param name: property name
        :type name: str
        :param scikit_time: time point, for scikit properties
        :type scikit_time: int
        :return:  the step value
        :rtype: int
        """
        max_step = self.get_number_of_curations()
        for step in reversed(range(0,max_step+1)):
            path = Path(join(self.temp_path, str(step)))
            if path.exists():
                # MorphoNet properties
                globtxt = path.glob("*.txt")
                for result in sorted(globtxt, key=lambda item: len(str(item))):
                    property_name = result.stem
                    if property_name == name:
                        return step
                # SCIKIT properties
                globpkl = path.glob("*.regions.pickle")
                for result in sorted(globpkl, key=lambda item: len(str(item))):
                    region_file = join(self.temp_path, str(step), result.name)
                    if scikit_time == -1:
                        with open(region_file, "rb") as infile:
                            prop = pickle.load(infile)
                            for cell_id in prop:
                                for property_name in prop[cell_id]:
                                    if property_name == name:
                                        return step
                    else:
                        timep = -1
                        if "_t" in result.name:
                            if "_ch" in result.name:
                                timep = int(result.name.split("_t")[-1].split("_ch")[0])
                                chp = int(result.name.split("_ch")[-1].split(".")[0])
                            else:
                                timep = int(result.name.split("_t")[-1].split(".")[0])
                                chp = 0
                        if timep != -1 and scikit_time == timep:
                            with open(region_file, "rb") as infile:
                                prop = pickle.load(infile)
                                for cell_id in prop:
                                    for property_name in prop[cell_id]:
                                        if property_name == name:
                                            return step
        return 0

    def find_properties_path_at_step_no_name(self, current_step, scikit_time=-1,ch=-1):
        """
        Returns the path to the last updated property file for a given name, for a given step.
        (search will be done from given step to 0  returning the first found)
        Time can be added, if time is not specified, returns the last step found for the curation name. If specified,
        will find the last step for a scikit property at given time

        :param name: property name
        :type name: str
        :current_step: Current step
        :type current_step: int
        :param scikit_time: time point, for scikit properties
        :type scikit_time: int
        :param ch: channel for scikit properties
        :type ch: int
        :param scikit_only: if True will only find the last step for a scikit property
        :type scikit_only: bool
        :return: The path to property file
        :rtype: str
        """
        for step in reversed(range(0,current_step+1)):
            path = Path(join(self.temp_path, str(step)))
            if path.exists():
                # SCIKIT properties
                globpkl = path.glob("*.regions.pickle")
                for result in sorted(globpkl, key=lambda item: len(str(item))):
                    region_file = join(self.temp_path, str(step), result.name)
                    if scikit_time == -1:
                        return region_file
                    else:
                        timep = -1
                        chp = -1
                        if "_t" in result.name:
                            if "_ch" in result.name:
                                timep = int(result.name.split("_t")[-1].split("_ch")[0])
                                chp = int(result.name.split("_ch")[-1].split(".")[0])
                            else:
                                timep = int(result.name.split("_t")[-1].split(".")[0])
                                chp = 0
                        if timep != -1 and scikit_time == timep and (ch == -1 or ch == chp):
                            return region_file
        return None
    def find_property_path_at_step(self, name, current_step, scikit_time=-1,ch=-1,scikit_only=False):
        """
        Returns the path to the last updated property file for a given name, for a given step.
        (search will be done from given step to 0  returning the first found)
        Time can be added, if time is not specified, returns the last step found for the curation name. If specified,
        will find the last step for a scikit property at given time

        :param name: property name
        :type name: str
        :current_step: Current step
        :type current_step: int
        :param scikit_time: time point, for scikit properties
        :type scikit_time: int
        :param ch: channel for scikit properties
        :type ch: int
        :param scikit_only: if True will only find the last step for a scikit property
        :type scikit_only: bool
        :return: The path to property file
        :rtype: str
        """
        for step in reversed(range(0,current_step+1)):
            path = Path(join(self.temp_path, str(step)))
            if path.exists():
                # MorphoNet properties
                if not scikit_only:
                    globtxt = path.glob("*.txt")
                    for result in sorted(globtxt, key=lambda item: len(str(item))):
                        property_name = result.stem
                        if property_name == name:
                            return join(self.temp_path, str(step), result.name)
                # SCIKIT properties
                globpkl = path.glob("*.regions.pickle")
                for result in sorted(globpkl, key=lambda item: len(str(item))):
                    region_file = join(self.temp_path, str(step), result.name)
                    if scikit_time == -1:
                        with open(region_file, "rb") as infile:
                            prop = pickle.load(infile)
                            for cell_id in prop:
                                for property_name in prop[cell_id]:
                                    if property_name == name:
                                        return region_file
                    else:
                        timep = -1
                        chp = -1
                        #print(result.name)
                        if "_t" in result.name:
                            if "_ch" in result.name:
                                timep = int(result.name.split("_t")[-1].split("_ch")[0])
                                chp = int(result.name.split("_ch")[-1].split(".")[0])
                            else:
                                timep = int(result.name.split("_t")[-1].split(".")[0])
                                chp = 0
                        #print(str(timep)+" - "+str(chp))
                        if timep != -1 and scikit_time == timep and (ch == -1 or ch == chp):
                            with open(region_file, "rb") as infile:
                                prop = pickle.load(infile)
                                for cell_id in prop:
                                    for property_name in prop[cell_id]:
                                        if property_name == name:
                                            return region_file
        return None

    def get_segmentation(self,time,step=-1,channel=0,load_array=True):
        """
        Return the segmentation specified object by time,channel at a given step (if -1, use the last step found).
        If load_array is set to False, the image content will not be loaded into the segmentation object

        :param time: time point
        :type time: int
        :param step: step  ( if -1, use the last step found)
        :type step: int
        :param channel: channel
        :type channel: int
        :param load_array: Should the function load the image content into the segmentation object ? True by default
        :type load_array: bool

        :return: segmentation object
        :rtype: Segmentation
        """
        if self.min_time > time or self.max_time < time:
            print("Time is out of dataset time points")
            return None
        prop_step = step
        if step == -1:
            prop_step = self.get_segmentation_last_step(time,channel)
        return self.get_segmentation_at_step(time,prop_step,channel,load_array)

    def get_segmentation_at_step(self,time, step, channel=0,load_array=True):
        """
        Return the segmentation specified object by time,channel at a specific given step.
        If load_array is set to False, the image content will not be loaded into the segmentation object

        :param time: time point
        :type time: int
        :param step: step
        :type step: int
        :param channel: channel
        :type channel: int
        :param load_array: Should the function load the image content into the segmentation object ? True by default
        :type load_array: bool

        :return: segmentation object
        :rtype: Segmentation
        """
        segmentation_object = None
        if step in self.steps:
            if self.steps[step].contains_segmentation_image_at(time,channel):
                return self.steps[step].get_segmentation_image(time,channel)
        path = self.find_segmentation_path_at_step(step,time,channel)
        if path is not None:
            if os.path.isfile(path):
                img = [x for x in self.list_images_temp if x.channel == channel and x.time_point == time]
                if len(img) > 0:
                    segmentation_object = copy.deepcopy(img[0])
                    segmentation_object.image_temp_path = path
                else:
                    image_name = ""
                    image_original_time = time
                    image_original_channel = channel
                    image_time = time
                    image_channel = channel
                    image_voxel_size = []
                    image_size = []
                    image_encoding = []
                    segmentation_object = Image(image_channel, image_time, image_name, image_original_channel, image_original_time,
                                path, image_voxel_size, image_size, image_encoding, path,None)
                if segmentation_object is not None:
                    img_np = np.load(path)
                    if len(segmentation_object.size) == 0:
                        segmentation_object.size = img_np.size
                    if len(segmentation_object.voxel_size) == 0:
                        segmentation_object.voxel_size = img_np.voxel_size
                    if len(segmentation_object.encoding) == 0:
                        segmentation_object.encoding = img_np.encoding
                    if load_array:
                        img_array = img_np['data']
                        segmentation_object.ndarray = img_array
                    if not step in self.steps:
                        step_folder = os.path.join(self.temp_path, str(step))
                        action_file = os.path.join(step_folder, "action")
                        self.steps[step] = DatasetStep(self, step, step_folder, action_file)
                    self.steps[step].add_segmentation(segmentation_object)
        return segmentation_object

    def find_properties_path_at_step(self, current_step, scikit_time=-1,include_scikit=True):
        """
        Find all properties file path for property in current_step, can include scikit properties or not.
        For a scikit property, can be filtered on time point using "t" parameter
        If not found, return empty list.


        :param current_step: step to search in
        :type current_step: int
        :param scikit_time: time point if laoding a scikit property
        :type scikit_time: int
        :param include_scikit: should include scikit properties or not
        :type include_scikit: bool

        :return: list of paths to properties file
        :rtype: list
        """
        list_properties_path = []
        path = Path(join(self.temp_path, str(current_step)))
        if path.exists():
            # MorphoNet properties
            globtxt = path.glob("*.txt")
            for result in sorted(globtxt, key=lambda item: len(str(item))):
                list_properties_path.append(join(self.temp_path, str(current_step), result.name))
            # SCIKIT properties
            if include_scikit:
                globpkl = path.glob("*.regions.pickle")
                for result in sorted(globpkl, key=lambda item: len(str(item))):
                    region_file = join(self.temp_path, str(current_step), result.name)
                    if scikit_time == -1:
                        list_properties_path.append(region_file)
                    else:
                        timep = -1
                        if "_t" in result.name:
                            if "_ch" in result.name:
                                timep = int(result.name.split("_t")[-1].split("_ch")[0])
                                chp = int(result.name.split("_ch")[-1].split(".")[0])
                            else:
                                timep = int(result.name.split("_t")[-1].split(".")[0])
                                chp = 0
                        if timep != -1 and scikit_time != -1 and scikit_time == timep:
                            list_properties_path.append(region_file)
        return list_properties_path

    def get_updated_properties(self, step=-1, scikit_time=-1, include_scikit=True):
        """
        Returns all properties found at step parameter. If step is -1, returns all properties at last step.
        Can include scikit properties or not.
        For a scikit property, can be filtered on time point using "t" parameter
        If not found, return empty list.

        :param step: step to search. If -1 or not specified, search for last step
        :type step: int
        :param scikit_time: time point if laoding a scikit property
        :type scikit_time: int
        :param include_scikit: should include scikit properties or not
        :type include_scikit: bool
        :return: all properties found at step parameter
        :rtype: dict
        """
        img_step = step
        if step == -1:
            img_step = self.get_number_of_curations()
        property_objects = []
        path_list = self.find_properties_path_at_step(img_step,scikit_time=scikit_time,include_scikit=include_scikit)
        for path in path_list:
            if path is not None:
                if path.endswith(".txt"):
                    already_exist = False
                    property_name = path.split(os.sep)[-1].split(".")[0]
                    property_object = None
                    for prop_tmp in property_objects:
                        if prop_tmp.name == property_name:
                            property_object = prop_tmp
                            already_exist = True
                    if property_object is None:
                        if img_step  not in self.steps:
                            step_folder = os.path.join(self.temp_path, str(img_step))
                            action_file = os.path.join(step_folder, "action")
                            self.steps[img_step] = DatasetStep(self, img_step, step_folder, action_file)
                        property_object = self.steps[img_step].add_property(property_name, path, "")
                    property_object.load_from_txt(path)
                    if not already_exist:
                        property_objects.append(property_object)
                else:
                    if include_scikit:
                        property_names = list_properties_in_pickle(path)
                        for name in property_names:
                            already_exist = False
                            property_object = None
                            for prop_tmp in property_objects:
                                if prop_tmp.name == name:
                                    property_object = prop_tmp
                                    already_exist = True
                            if property_object is None:
                                if img_step not in self.steps:
                                    step_folder = os.path.join(self.temp_path, str(img_step))
                                    action_file = os.path.join(step_folder, "action")
                                    self.steps[img_step] = DatasetStep(self, img_step, step_folder, action_file)
                                property_object = self.steps[img_step].add_property(name, path, "")
                            if scikit_time == -1:
                                for time_temp in range(self.min_time,self.max_time+1):
                                    path_at_time = self.find_property_path_at_step(name, img_step,scikit_time=scikit_time)
                                    if path_at_time is not None:
                                        property_object.load_from_scikit(path_at_time,time_temp)
                            else:
                                property_object.load_from_scikit(path,scikit_time)
                            if property_object is not None:
                                if not already_exist:
                                    property_objects.append(property_object)
        return property_objects

    def list_all_properties(self):
        """
        List all properties available in the dataset

        :return: all properties found at step parameter
        :rtype: dict
        """
        img_step = self.get_number_of_curations()
        final_property_names = []
        for step_temp in reversed(range(0, img_step + 1)):
            path_list = self.find_properties_path_at_step(step_temp)
            for path in path_list:
                if path is not None:
                    if path.endswith(".txt"):
                        already_exist = False
                        property_name = path.split(os.sep)[-1].split(".")[0]
                        if not property_name in final_property_names:
                            final_property_names.append(property_name)
                    else:
                        # print(path)
                        property_names = list_properties_in_pickle(path)
                        for name in property_names:
                            if not name in final_property_names:
                                final_property_names.append(name)
        return list(sorted(final_property_names))

    def get_all_properties(self, step=-1, scikit_time=-1, include_scikit=True):
        """
        Returns all properties found at step parameter, including all steps before. If step is -1, returns all properties at last step.
        Can include scikit properties or not.
        For a scikit property, can be filtered on time point using "t" parameter
        If not found, return empty list.

        :param step: step to search. If -1 or not specified, search for last step
        :type step: int
        :param scikit_time: time point if laoding a scikit property
        :type scikit_time: int
        :param include_scikit: should include scikit properties or not
        :type include_scikit: bool
        :return: all properties found at step parameter
        :rtype: dict
        """
        img_step = step
        if step == -1:
                img_step = self.get_number_of_curations()
        property_objects = []
        for step_temp in reversed(range(0,img_step+1)):
            print("Reading step : "+str(step_temp))
            path_list = self.find_properties_path_at_step(step_temp, scikit_time=scikit_time,include_scikit=include_scikit)
            for path in path_list:
                if path is not None:
                    if path.endswith(".txt"):
                        already_exist = False
                        property_name = path.split(os.sep)[-1].split(".")[0]
                        property_object = None
                        for prop_tmp in property_objects:
                            if prop_tmp.name == property_name:
                                property_object = prop_tmp
                                already_exist = True
                        if property_object is None:
                            if step_temp not in self.steps:
                                step_folder = os.path.join(self.temp_path, str(step_temp))
                                action_file = os.path.join(step_folder, "action")
                                self.steps[step_temp] = DatasetStep(self, step_temp, step_folder, action_file)
                            property_object = self.steps[step_temp].add_property(property_name, path, "")
                        property_object.load_from_txt(path)
                        if not already_exist:
                            property_objects.append(property_object)
                    else:
                        if include_scikit:
                            #print(path)
                            property_names = list_properties_in_pickle(path)
                            for name in property_names:
                                #print("found prop name : "+str(name))
                                already_exist = False
                                property_object = None
                                for prop_tmp in property_objects:
                                    if prop_tmp.name == name:
                                        property_object = prop_tmp
                                        already_exist = True
                                if property_object is None:
                                    if step_temp not in self.steps:
                                        step_folder = os.path.join(self.temp_path, str(step_temp))
                                        action_file = os.path.join(step_folder, "action")
                                        self.steps[step_temp] = DatasetStep(self, step_temp, step_folder, action_file)
                                    property_object = self.steps[step_temp].add_property(name, path, "")
                                if scikit_time == -1:
                                    for time_temp in range(self.min_time, self.max_time + 1):
                                        path_at_time = self.find_property_path_at_step(name, step_temp, scikit_time=time_temp)
                                        if path_at_time is not None:
                                            #print("loading at time : "+str(time_temp))
                                            property_object.load_from_scikit(path_at_time, time_temp)
                                else:
                                    #print("loading from specific time : "+str(time))
                                    property_object.load_from_scikit(path, scikit_time)
                                if property_object is not None:
                                    if not already_exist:
                                        property_objects.append(property_object)
                                        #print(len(property_object.values))
        return property_objects


    def print_computable_properties(self):
        """
        Print all properties that can be computed using compute_property commands
        """
        list_props = get_all_regionprop_names()
        print(list_props)

    def compute_property_all_steps(self, property_name, ch=0,save=True):
        """
        Compute the region property for all available steps, for all time points.
        The computed region properties will be saved  to temporary folder in MorphoNet.

        :param property_name: Name of the property
        :type property_name: str
        :param ch: channel index for the property computation
        :type ch: int
        :param save: should save the property to file? (optional, default is True)
        :type save: bool
        :return: Property computed
        :rtype: DataProperty
        """
        print("Computing "+str(property_name)+" for all steps in the embryo , this may take a while")
        if not is_property_a_regionprop(property_name):
            print("The property to compute is not among possible properties : ")
            self.print_computable_properties()
            exit()
        for step in range(0,self.get_number_of_curations()+1):
            self.compute_property(property_name,step,ch,save)

    def compute_property(self, property_name, step=-1,ch=0,save=True):
        """
        Compute the region property for a given step, for all time points.
        The computed region properties will be saved  to temporary folder in MorphoNet.

        :param property_name: Name of the property
        :type property_name: str
        :param step: step to find the property version, -1 for last step
        :type step: int
        :param ch: channel index for the property computation
        :type ch: int
        :param save: should save the property to file? (optional, default is True)
        :type save: bool
        :return: Property computed
        :rtype: DataProperty
        """
        found_property = None
        if not is_property_a_regionprop(property_name):
            print("The property to compute is not among possible properties : ")
            self.print_computable_properties()
            exit()
        for timep in range(self.min_time,self.max_time+1):
            property_t = self.compute_property_at(property_name,timep,step,ch,save=save)
            if property_t is not None:
                if found_property is None:
                    ptype = get_property_type(property_name)
                    found_property = DataProperty(self, property_name, "", ptype)
                if property_t.get_step(timep) is not None:
                    found_property.set_step(property_t.get_step(timep), timep)
                if property_t.get_path(timep) is not None:
                    found_property.set_path(property_t.get_path(timep), timep)
                #print(property_t.get_keys())
                for cell_key in property_t.get_keys():
                    #print("aaaaaaaa")
                    #print(cell_key)
                    tc,idc,chanc = get_object_t_id_ch(cell_key)
                    found_property.set_object_value(tc,idc,chanc,property_t.get_object_value(tc,idc,chanc))
        return found_property

    def compute_property_at(self, property_name, time, step=-1, ch=0,save=True):
        """
        Compute the region property for a given step, at given time point.
        The computed region properties will be saved  to temporary folder in MorphoNet.

        :param property_name: Name of the property
        :type property_name: str
        :param time: time point
        :type time: int
        :param step: step to find the property version, -1 for last step
        :type step: int
        :param ch: channel index for the property computation
        :type ch: int
        :param save: should save the property to file? (optional, default is True)
        :type save: bool
        :return: segmentation image array corresponding to time point and channel, for step
        :rtype: DataProperty
        """
        if not is_property_a_regionprop(property_name):
            print("The property to compute is not among possible properties : ")
            print(get_all_regionprop_names())
            exit()
        img_step = step
        if step == -1:
            img_step = self.get_segmentation_last_step(time, ch)
        if property_name == "lineage_distance":
            return self._compute_lineage_distance_at_time_step(img_step,time,ch,save=save)
        else:
            return self.compute_property_at_time_step(property_name, img_step, time,ch,save=save)
    def _compute_lineage_distance_at_time_step(self,step,time,ch=0,save=True):
        property_object = DataProperty(self, "lineage_distance", "", "float")
        path = self.find_properties_path_at_step_no_name( step, scikit_time=time, ch=ch)
        existing_regions = {}
        if path is not None and os.path.exists(path):
            print("A region file already exist, will load first and than add new property")
            step = int(path.split(os.sep)[-2])
            with open(path, "rb") as infile:
                # print("loading file")
                prop = pickle.load(infile)
                for cell_id in prop:
                    for p in prop[cell_id]:
                        if p != "lineage_distance":
                            if not cell_id in existing_regions:
                                existing_regions[cell_id] = {}
                            existing_regions[cell_id][p] = prop[cell_id][p]
        else :
            print("No region file found, creating it")
            seg = self.find_segmentation_path_at_step(step, time, ch=ch)
            path = seg.replace(".npz",".regions.pickle")

        import edist.ted
        import edist.uted as uted

        # Retrieve CellName property
        property_name = self.get_property_at_time_step("cell_name",step,time)
        if property_name is None:
            print("No cell naming found. Names are needed for lineage distance")
            return None

        cell_lineage = self.get_property_at_time_step("cell_lineage",step,time)
        if cell_lineage is None:
            cell_lineage = self.get_property_at_time_step("temporal",step,time)
            if cell_lineage is None:
                print("No cell lineage found. Lineage are needed for lineage distance")
                return None
        def local_cost_normalized(x, y):
            if x is None and y is None:
                return 0
            elif x is None or y is None:
                return 1
            elif x not in x_nodes or y not in y_nodes:
                return 1
            xl = x_life[x_nodes.index(x)]
            yl = y_life[y_nodes.index(y)]
            return abs(xl - yl) / (xl + yl)

        # LINEAGE COMPARISON
        #if not cell_id in existing_regions:
        #existing_regions[cell_id] = {}

        for cell_key in property_name.get_keys():
            name = property_name.values[cell_key]
            #print("Trying to compute lineage dist for cell "+str(cell_key)+" with name : "+str(name))
            if name is not None and name.endswith("*"):  # ONLY GET RIGHT SIDE
                #print("found cell on right side ")
                #print("working time is "+str(time))
                tc,idc,chanc = get_object_t_id_ch(cell_key)
                if int(tc) == int(time):
                    #print("found cell at time : "+str(tc)+" with id "+str(idc))
                    smo = get_symetric_cells(tc,property_name, name)
                    #print("smo : "+str(smo))
                    #print("cell_key : "+str(cell_key))
                    if smo is not None:
                        ts,ids,chans = get_object_t_id_ch(smo)
                        x_nodes, x_adj, x_life = get_node(cell_lineage,cell_key)
                        y_nodes, y_adj, y_life = get_node(cell_lineage,smo)
                        d = uted.uted(x_nodes, x_adj, y_nodes, y_adj, local_cost_normalized)
                        final_cell_key = get_longid(int(tc),int(idc))
                        final_smo = get_longid(int(ts),int(ids))
                        if not final_cell_key in existing_regions:
                            existing_regions[final_cell_key] = {}
                        if not final_smo in existing_regions:
                            existing_regions[final_smo] = {}
                        existing_regions[final_cell_key]["lineage_distance"] = d
                        existing_regions[final_smo]["lineage_distance"] = d
        #print(existing_regions)
        if save:
            print("Saving computed property in file : " + str(path))
            with open(path, "wb") as outfile:  # Save region prop
                pickle.dump(existing_regions, outfile)
            # WE SHOULD ADD MORE COMPUTATION (not only region props)
        #print(existing_regions)
        for region_cell in existing_regions:
            for prop_name in existing_regions[region_cell]:
                if prop_name == "lineage_distance":
                    #print(region_cell)
                    trc,idrc = get_id_t(region_cell)
                    property_object.set_object_value(trc, idrc, ch, existing_regions[region_cell][prop_name])
        property_object.set_path(path,time)
        property_object.set_step(step,time)
        return property_object

    def delete_property_all_steps(self, property_name, ch=0):
        """
        Delete the region property at all steps, for all time points.

        :param property_name: Name of the property
        :type property_name: str
        :param ch: channel index for the property computation
        :type ch: int
        """
        print("Deleting "+str(property_name)+" for all steps, this may take a while")
        for step in range(0,self.get_number_of_curations()+1):
            self.delete_property(property_name,step,ch)
    def delete_property(self, property_name, step=-1,ch=0):
        """
        Delete the region property for a given step, for all time points.

        :param property_name: Name of the property
        :type property_name: str
        :param step: step to find the property version, -1 for last step
        :type step: int
        :param ch: channel index for the property computation
        :type ch: int
        """
        for timep in range(self.min_time,self.max_time+1):
            self.delete_property_at(property_name,timep,step,ch)

    def delete_property_at(self, property_name, time, step=-1, ch=0):
        """
        Delete the region property for a given step, at given time point.

        :param property_name: Name of the property
        :type property_name: str
        :param time: time point
        :type time: int
        :param step: step to find the property version, -1 for last step
        :type step: int
        :param ch: channel index for the property computation
        :type ch: int
        """
        img_step = step
        if step == -1:
            img_step = self.get_segmentation_last_step(time, ch)
        return self.delete_property_at_time_step(property_name, img_step, time,ch)

    def delete_property_at_time_step(self, property_name, step, time, ch=0):
        """
        Delete the property asked for segmentation at time and step.
        Reads a potential existing properties file, and remvoe the property

        :param property_name: Name of the property
        :type property_name: str
        :param time: time point
        :type time: int
        :param step: step to find the property version, -1 for last step
        :type step: int
        :param ch: channel index for the property computation
        :type ch: int
        """
        print("Deleting property " + str(property_name) + " at step : " + str(step) + " for time " + str(
            time) + " and channel " + str(ch))
        path = self.find_property_path_at_step(property_name, step, scikit_time=time, ch=ch, scikit_only=True)
        existing_regions = {}
        if path is not None and os.path.exists(path):
            step = int(path.split(os.sep)[-2])
            with open(path, "rb") as infile:
                # print("loading file")
                prop = pickle.load(infile)
                for cell_id in prop:
                    for p in prop[cell_id]:
                        if property_name != p:
                            if not cell_id in existing_regions:
                                existing_regions[cell_id] = {}
                            existing_regions[cell_id][p] = prop[cell_id][p]
            # WE SHOULD ADD MORE COMPUTATION (not only region props)
            print("Saving deleted property in file : " + str(path))
            with open(path, "wb") as outfile:  # Save region prop
                pickle.dump(existing_regions, outfile)
    def compute_property_at_time_step(self, property_name, step, time,ch=0,save=True):
        """
        Compute the property asked for segmentation at time and step.
        Reads a potential existing properties file, load them, compute the info and add it to the file

        :param property_name: Name of the property
        :type property_name: str
        :param time: time point
        :type time: int
        :param step: step to find the property version, -1 for last step
        :type step: int
        :param ch: channel index for the property computation
        :type ch: int
        :param save: should save the property to file? (optional, default is True)
        :type save: bool
        :return: New property created
        :rtype: DataProperty
        """
        if not is_property_a_regionprop(property_name):
            print("The property to compute is not among possible properties : ")
            print(get_all_regionprop_names())
            exit()
        print("Computing property "+str(property_name)+" at step : "+str(step)+" for time "+str(time)+" and channel "+str(ch))
        property_object = DataProperty(self, property_name, "", get_property_type(property_name))
        path = self.find_properties_path_at_step_no_name(step,scikit_time=time,ch=ch)
        existing_regions = {}
        if path is not None and os.path.exists(path):
            step = int(path.split(os.sep)[-2])
            with open(path, "rb") as infile:
                # print("loading file")
                prop = pickle.load(infile)
                for cell_id in prop:
                    for p in prop[cell_id]:
                        if property_name != p:
                            if not cell_id in existing_regions:
                                existing_regions[cell_id] = {}
                            existing_regions[cell_id][p] = prop[cell_id][p]
            seg = self.find_segmentation_path_at_step(step, time, ch=ch)
            print(seg)
            seg_array = np.load(seg)['data']
            #reg = regionprops(seg_array)
            if property_name == "connected_neighbors":
                region = regionprops(seg_array)
                for reg in region:
                    elt = reg['label']
                    value = connected_neighbors(reg, seg_array, self.background_value)
                    if not elt in existing_regions:
                        existing_regions[elt] = {}
                    existing_regions[elt][property_name] = value
            elif property_name == "roughness":
                region = regionprops(seg_array)
                for reg in region:
                    elt = reg['label']
                    value = roughness(reg, seg_array)
                    if not elt in existing_regions:
                        existing_regions[elt] = {}
                    existing_regions[elt][property_name] = value
            elif property_name == "intensity_offset":
                region = regionprops(seg_array)
                raw_data = self.get_intensity_image(time,ch).ndarray
                for reg in region:
                    elt = reg['label']
                    value = intensity_offset(reg, raw_data)
                    if not elt in existing_regions:
                        existing_regions[elt] = {}
                    existing_regions[elt][property_name] = value
            elif property_name == "intensity_border_variation":
                region = regionprops(seg_array)
                raw_data = self.get_intensity_image(time, ch).ndarray
                for reg in region:
                    elt = reg['label']
                    value = intensity_border_variation(reg, seg_array,raw_data)
                    if not elt in existing_regions:
                        existing_regions[elt] = {}
                    existing_regions[elt][property_name] = value
            elif property_name == "axis_ratio":
                region = regionprops(seg_array)
                for reg in region:
                    elt = reg['label']
                    value = axis_ratio(reg)
                    if not elt in existing_regions:
                        existing_regions[elt] = {}
                    existing_regions[elt][property_name] = value
            elif property_name == "diameter":
                region = regionprops(seg_array)
                for reg in region:
                    elt = reg['label']
                    value = diameter(reg)
                    if not elt in existing_regions:
                        existing_regions[elt] = {}
                    existing_regions[elt][property_name] = value
            elif property_name == "convexity":
                region = regionprops(seg_array)
                for reg in region:
                    elt = reg['label']
                    value = convexity(reg)
                    if not elt in existing_regions:
                        existing_regions[elt] = {}
                    existing_regions[elt][property_name] = value
            elif property_name == "compactness":
                region = regionprops(seg_array)
                for reg in region:
                    elt = reg['label']
                    value = compactness(reg)
                    if not elt in existing_regions:
                        existing_regions[elt] = {}
                    existing_regions[elt][property_name] = value
            elif property_name == "smoothness":
                region = regionprops(seg_array)
                for reg in region:
                    elt = reg['label']
                    value = smoothness(reg)
                    if not elt in existing_regions:
                        existing_regions[elt] = {}
                    existing_regions[elt][property_name] = value
            elif property_name == "mother-daughter-ratio":
                if time > self.min_time:
                    prevpath = self.find_properties_path_at_step_no_name(step, scikit_time=time-1, ch=ch)
                    if prevpath is not None and os.path.exists(prevpath):
                        step = int(prevpath.split(os.sep)[-2])
                        with open(prevpath, "rb") as infile:
                            # print("loading file")
                            prev_region = pickle.load(infile)
                    else:
                        prevseg = self.find_segmentation_path_at_step(step, time - 1, ch=ch)
                        prev_seg_array = np.load(prevseg)['data']
                        prev_region = {}
                        prev_region_loaded = regionprops(prev_seg_array)
                        for reg in prev_region_loaded:
                            elt = reg['label']
                            prev_region[elt] = {}
                            for p_name in reg:
                                if p_name != 'label':
                                    prev_region[elt][p_name] = reg[p_name]
                    region = regionprops(seg_array)

                    lineage_property = self.get_property("temporal")
                    if lineage_property is None:
                        lineage_property = self.get_property("cell_lineage")
                    for reg in region:
                        elt = reg['label']
                        cell_key = get_object_id(time,elt,ch)
                        cell_mother_key = get_previous_cell_in_lineage(cell_key, lineage_property)
                        volume_elem = None
                        if 'area' in reg:
                            volume_elem = reg['area']
                        elif 'volume' in reg:
                            volume_elem = reg['volume']
                        if cell_mother_key is not None:
                            m_t, m_id, m_c = get_object_t_id_ch(cell_mother_key)
                            if int(m_id) in prev_region:
                                volume_prev = None
                                if 'volume' in prev_region[int(m_id)]:
                                    volume_prev = prev_region[int(m_id)]['volume']
                                elif 'area' in prev_region[int(m_id)]:
                                    volume_prev = prev_region[int(m_id)]['area']
                                if volume_prev is not None and volume_elem is not None and volume_elem != 0:
                                    value = volume_prev / volume_elem
                                    if not elt in existing_regions:
                                        existing_regions[elt] = {}
                                    existing_regions[elt][property_name] = value

            else:
                reg = regionprops_table(seg_array, properties=['label', property_name])
                #property_list = [x for x in reg.keys() if x != "label"]
                #print(property_list)
                num_regions = len(reg['label'])
                for i in range(num_regions):
                    elt = reg['label'][i]
                    value = reg[property_name][i]
                    if elt != self.background_value:
                        if not elt in existing_regions:
                            existing_regions[elt] = {}
                        existing_regions[elt][property_name] = value
            # WE SHOULD ADD MORE COMPUTATION (not only region props)
        else:
            seg = self.find_segmentation_path_at_step(step, time, ch=ch)
            seg_array = np.load(seg)['data']
            path = seg.replace(".npz",".regions.pickle")
            if property_name == "connected_neighbors":
                region = regionprops(seg_array)
                for reg in region:
                    elt = reg['label']
                    value = connected_neighbors(reg, seg_array, self.background_value)
                    if not elt in existing_regions:
                        existing_regions[elt] = {}
                    existing_regions[elt][property_name] = value
            elif property_name == "roughness":
                region = regionprops(seg_array)
                for reg in region:
                    elt = reg['label']
                    value = roughness(reg, seg_array)
                    if not elt in existing_regions:
                        existing_regions[elt] = {}
                    existing_regions[elt][property_name] = value
            elif property_name == "intensity_offset":
                region = regionprops(seg_array)
                raw_data = self.get_intensity_image(time,ch).ndarray
                for reg in region:
                    elt = reg['label']
                    value = intensity_offset(reg, raw_data)
                    if not elt in existing_regions:
                        existing_regions[elt] = {}
                    existing_regions[elt][property_name] = value
            elif property_name == "intensity_border_variation":
                region = regionprops(seg_array)
                raw_data = self.get_intensity_image(time, ch).ndarray
                for reg in region:
                    elt = reg['label']
                    value = intensity_border_variation(reg, seg_array,raw_data)
                    if not elt in existing_regions:
                        existing_regions[elt] = {}
                    existing_regions[elt][property_name] = value
            elif property_name == "axis_ratio":
                region = regionprops(seg_array)
                for reg in region:
                    elt = reg['label']
                    value = axis_ratio(reg)
                    if not elt in existing_regions:
                        existing_regions[elt] = {}
                    existing_regions[elt][property_name] = value
            elif property_name == "diameter":
                region = regionprops(seg_array)
                for reg in region:
                    elt = reg['label']
                    value = diameter(reg)
                    if not elt in existing_regions:
                        existing_regions[elt] = {}
                    existing_regions[elt][property_name] = value
            elif property_name == "convexity":
                region = regionprops(seg_array)
                for reg in region:
                    elt = reg['label']
                    value = convexity(reg)
                    if not elt in existing_regions:
                        existing_regions[elt] = {}
                    existing_regions[elt][property_name] = value
            elif property_name == "compactness":
                region = regionprops(seg_array)
                for reg in region:
                    elt = reg['label']
                    value = compactness(reg)
                    if not elt in existing_regions:
                        existing_regions[elt] = {}
                    existing_regions[elt][property_name] = value
            elif property_name == "smoothness":
                region = regionprops(seg_array)
                for reg in region:
                    elt = reg['label']
                    value = smoothness(reg)
                    if not elt in existing_regions:
                        existing_regions[elt] = {}
                    existing_regions[elt][property_name] = value
            elif property_name == "mother-daughter-ratio":
                if time > self.min_time:
                    prevpath = self.find_properties_path_at_step_no_name(step, scikit_time=time-1, ch=ch)
                    if prevpath is not None and os.path.exists(prevpath):
                        step = int(prevpath.split(os.sep)[-2])
                        with open(prevpath, "rb") as infile:
                            # print("loading file")
                            prev_region = pickle.load(infile)
                    else:
                        prevseg = self.find_segmentation_path_at_step(step, time - 1, ch=ch)
                        prev_seg_array = np.load(prevseg)['data']
                        prev_region = {}
                        prev_region_loaded = regionprops(prev_seg_array)
                        for reg in prev_region_loaded:
                            elt = reg['label']
                            prev_region[elt] = {}
                            for p_name in reg:
                                if p_name != 'label':
                                    prev_region[elt][p_name] = reg[p_name]

                    region = regionprops(seg_array)

                    lineage_property = self.get_property("temporal")
                    if lineage_property is None:
                        lineage_property = self.get_property("cell_lineage")

                    for reg in region:
                        elt = reg['label']
                        cell_key = get_object_id(time, elt, ch)
                        cell_mother_key = get_previous_cell_in_lineage(cell_key, lineage_property)
                        volume_elem = None
                        if 'area' in reg:
                            volume_elem = reg['area']
                        elif 'volume' in reg:
                            volume_elem = reg['volume']
                        if cell_mother_key is not None:
                            m_t, m_id, m_c = get_object_t_id_ch(cell_mother_key)
                            if int(m_id) in prev_region:
                                volume_prev = None
                                if 'volume' in prev_region[int(m_id)]:
                                    volume_prev = prev_region[int(m_id)]['volume']
                                elif 'area' in prev_region[int(m_id)]:
                                    volume_prev = prev_region[int(m_id)]['area']
                                if volume_prev is not None and volume_elem is not None and volume_elem != 0:
                                    value = volume_prev / volume_elem
                                    if not elt in existing_regions:
                                        existing_regions[elt] = {}
                                    existing_regions[elt][property_name] = value
            else:
                reg = regionprops_table(seg_array, properties=['label',property_name])
                num_regions = len(reg['label'])
                for i in range(num_regions):
                    elt = reg['label'][i]
                    value = reg[property_name][i]
                    if elt != self.background_value:
                        if not elt in existing_regions:
                            existing_regions[elt] = {}
                        existing_regions[elt][property_name] = value
        if save:
            print("Saving computed property in file : " + str(path))
            with open(path, "wb") as outfile:  # Save region prop
                pickle.dump(existing_regions, outfile)
            # WE SHOULD ADD MORE COMPUTATION (not only region props)
        #print(existing_regions)
        for region_cell in existing_regions:
            for prop_name in existing_regions[region_cell]:
                if property_name == prop_name:
                    property_object.set_object_value(time, region_cell, ch, existing_regions[region_cell][prop_name])
        property_object.set_path(path,time)
        property_object.set_step(step,time)
        return property_object

    def get_property(self, property_name,step=-1):
        """
        Return the property object at given step. If step is -1, find in last step
        The time point parameter is only used loading a scikit properties

        :param property_name: Name of the property
        :type property_name: str
        :param step: step to find the property version, -1 for last step
        :type step: int
        :return: Property found
        :rtype: DataProperty
        """
        found_property = None
        for timep in range(self.min_time,self.max_time+1):
            property_t = self.get_property_at(property_name,timep,step)

            if property_t is not None:
                if found_property is None:
                    found_property = DataProperty(self, property_name, "", "")
                if property_t.get_step(timep) is not None:
                    found_property.set_step(property_t.get_step(timep),timep)
                if property_t.get_path(timep) is not None:
                    found_property.set_path(property_t.get_path(timep),timep)
                if found_property.type == "":
                    found_property.type = property_t.type
                for cell_key in property_t.get_keys():
                    tc,idc,chanc = get_object_t_id_ch(cell_key)
                    found_property.set_object_value(tc,idc,chanc,property_t.get_object_value(tc,idc,chanc))
        return found_property






    def get_property_at(self, property_name, time, step=-1):
        """
        Return the property find by name, corresponding to time point, and step
        if step is -1, the function finds the image in. Time point is only used for scikit properties

        :param property_name: Name of the property
        :type property_name: str
        :param time: time point
        :type time: int
        :param step: step to find the property version, -1 for last step
        :type step: int
        :return: segmentation image array corresponding to time point and channel, for step
        :rtype: DataProperty
        """
        img_step = step
        if step == -1:
            img_step = self.get_property_last_step(property_name,time)
        return self.get_property_at_time_step(property_name,img_step,time)
    def get_property_at_time_step(self, property_name, step, time):
        """
        Return the property find by name, corresponding to time point, and step.
        Time point is only used for scikit properties

        :param property_name: Name of the property
        :type property_name: str
        :param time: time point
        :type time: int
        :param step: step to find the property version, -1 for last step
        :type step: int
        :return: segmentation image array corresponding to time point and channel, for step
        :rtype: DataProperty
        """
        property_object = None
        path = self.find_property_path_at_step(property_name, step,scikit_time=time)
        if path is not None and os.path.exists(path):
            if property_object is None:
                property_object = DataProperty(self, property_name, path, "")
            if path.endswith(".txt"):
                property_object.load_from_txt(path,time)
            else:
                property_object.load_from_scikit(path,time)
        return property_object

    def print_all_segmentations(self,channel=0):
        """
        Print all segmentation images found in the dataset for a given channel, and print their path to file

        :param channel: channel
        :type channel: int
        """
        for time in range(self.min_time,self.max_time+1):
            print("Time : " + str(time))
            image = self.get_segmentation(time,channel=channel,load_array=False)
            print("  -> Segmentation image")
            print("     Time : " + str(image.time_point))
            print("     Channel : " + str(image.channel))
            print("     Temporary path : " + str(image.image_temp_path))
            print("     Input path : " + str(image.path))


    def print_all_intensity_images(self,channel=0):
        """
        Print all segmentation images found in the dataset for a given channel, and print their path to file

        :param channel: channel
        :type channel: int
        """
        for time in range(self.min_time,self.max_time+1):
            print("Time : " + str(time))
            image = self.get_intensity_image(time,channel=channel,load_array=False)
            print("  -> Intensity image")
            print("     Time : "+str(image.time_point))
            print("     Channel : " + str(image.channel))
            print("     Temporary path : "+str(image.image_temp_path))
            print("     Input path : "+str(image.path))
