import copy

from morphonet.data.utils import get_object_id, get_object_t_id_ch
from morphonet.tools import get_longid, natural_sort
import pickle
from os import sep

class DataProperty:
    """
    The DataProperty is the class with which you manipulate MorphoNet Properties in the data module
    """
    def __init__(self, dataset, name, temp_path, prop_type):
        """
        A property has a name, a dict for values (cell_identifier -> value), and a path to the temp file
        """
        self.dataset = dataset
        self.step_by_t = {}
        self.name = name
        self.values = {}
        self.type = prop_type
        self.path_by_t = {}
        self.loaded_from_txt = None

    def load_from_scikit(self, temp_path, time):
        """
        Load the property from a scikit properties file, at a specific time

        :param temp_path: Path to the txt file to load in temp
        :type temp_path: str
        :param time: Time to load the property
        :type time: int
        """
        channel = 0
        self.loaded_from_txt = False
        if len(self.get_values_at(time)) > 0:  # Values were already loaded
            #print("values already loaded")
            return
        filename = temp_path.split(sep)[-1]
        step = int(temp_path.split(sep)[-2])
        if "_t" in filename:
            if "_ch" in filename:
                channel = int(filename.split("_ch")[-1].split(".")[0])
        with open(temp_path, "rb") as infile:
            self.set_path(temp_path, time)
            #print("loading file")
            prop = pickle.load(infile)
            for cell_id in prop:
                for property_name in prop[cell_id]:
                    if property_name == self.name:
                        #print("found property for cell : "+str(cell_id))
                        # property = self.steps[step].add_property(property_name)
                        object_value = prop[cell_id][property_name]
                        self.set_object_value(time,cell_id, channel, object_value)
            self.set_step(step,time)


    def load_from_txt(self, temp_path, time=-1,min_time=-1,max_time=-1):
        """
        Load the property from a text file, already with morphonet format

        :param temp_path: Path to the txt file to load in temp
        :type temp_path: str
        :param time: Time to load the property, -1 for all times
        :type time: int
        """
        lines = []
        self.loaded_from_txt = True
        step = int(temp_path.split(sep)[-2])
        f = open(temp_path, 'r')
        lines = f.readlines()
        f.close()
        if time != -1:
            if len(self.get_values_at(time)) > 0:  # Values were already loaded
                return
        final_min_time = min_time
        if final_min_time == -1:
            final_min_time = self.dataset.get_min_time()
        final_max_time = max_time
        if final_max_time == -1:
            final_max_time = self.dataset.get_max_time()

        times_to_load = [i for i in range(final_min_time,final_max_time + 1) if
                         len(self.get_values_at(i)) == 0]
        if len(lines) > 0:
            self.set_path(temp_path, time)
            for line in lines:
                if line.startswith("#") or line == "":
                    continue
                elif line.strip().startswith("type:"):
                    type = line.split(":")[1].strip()
                    self.type = type
                else:
                    values = line.split(":")
                    cell_identifier = values[0].strip()
                    cell_keys = cell_identifier.split(",")
                    cell_value = values[1].strip()
                    if self.type == "float" or self.type == "numbers":
                        cell_value = float(values[1].strip())
                    if self.type == "dict" or self.name == "cell_contact_surface":
                        if len(values) > 2:
                            cell_value = (values[1],values[2])
                        else:
                            cell_value = values[1]
                    timec = int(cell_keys[0])
                    cellid = int(cell_keys[1])
                    cellchannel = 0
                    if len(cell_keys) > 2:
                        cellchannel = int(cell_keys[2])
                    if time == -1 or (timec == time and timec in times_to_load):
                        self.set_step(step, time)
                        self.set_object_value(timec,cellid, cellchannel, cell_value)

    def set_object_value(self, t, idc, ch, value):
        """
        Change value of cell in the property

        :param t: Time point of the object
        :type t: int
        :param ch: Channel of the object
        :type ch: int
        :param idc: Object ID in the segmentation
        :type idc: int
        :param value: Value of the object in the property
        """
        object_name = get_object_id(t, idc, ch)
        if self.type == "dict" or self.name == "cell_contact_surface":
            ckey = value[0]
            cvalue = value[1]
            if object_name not in self.values:
                self.values[object_name] = {}
            self.values[object_name][ckey] = cvalue
        else :
            if object_name not in self.values:
                self.values[object_name] = value
            else :
                if not isinstance(self.values[object_name],list):
                    new_val = copy.deepcopy(self.values[object_name])
                    self.values[object_name] = []
                    self.values[object_name].append(new_val)
                    if new_val != value:
                        self.values[object_name].append(value)
                else:
                    if not value in self.values[object_name]:
                        self.values[object_name].append(value)

    def remove_from_property(self, t, idc , ch):
        """
        Remove a specific cell from the property

        :param t: Time point of the object
        :type t: int
        :param ch: Channel of the object
        :type ch: int
        :param idc: Object ID in the segmentation
        :type idc: int
        """
        object_name = get_object_id(t, idc, ch)
        if object_name in self.values:
            del self.values[object_name]

    def set_path(self,path,time):
        """
        Set the current property path for time
        :param path: Path to the property
        :type path: str
        :param time: Time to load the property
        :type time: int

        """
        self.path_by_t[time] = path

    def get_path(self,time):
        """
        Return  path for given time
        :param time: Time to load the property
        :type time: int
        """
        if not time in self.path_by_t:
            return None
        return self.path_by_t[time]
    def set_step(self,step,time):
        """
        Set the current step used to load the property

        :param step: Step to load the property
        :type step: int
        :param time: Time
        :type time: int
        """

        self.step_by_t[time] = step

    def get_step(self,time):
        """
        Return the step found for time point

        :param time: Time
        :type time: int
        """
        if not time in self.step_by_t:
            return None
        return self.step_by_t[time]

    def get_values(self):
        """
        Return all the values of the property

        :return: List all values of the property
        :rtype: list
        """
        return list(self.values.values())

    def get_keys(self):
        """
        Return all the keys of the property (objects_names)

        :return: List all keys of the property
        """
        return list(self.values.keys())

    def get_object_value(self, t, idc, ch):
        """
        Retrieve value of cell in property

        :param t: Time point of the object
        :type t: int
        :param ch: Channel of the object
        :type ch: int
        :param idc: Object ID in the segmentation
        :type idc: int
        :return: Value of the object in the property, or None if not found

        """
        object_name = get_object_id(t, idc, ch)
        if object_name in self.values:
            return self.values[object_name]
        return None

    def generate_xml(self, tree):
        """
        Generate the XML node for the current property

        :param tree: XML tree to load the property in
        :type tree: xml.etree.ElementTree.Element
        :return: XML node for the complete property
        :rtype: xml.etree.ElementTree.Element
        """
        import xml.etree.ElementTree as ET
        xml_node_name = self.name
        if xml_node_name == "temporal":
            xml_node_name = "cell_lineage"
        if xml_node_name == "volume_scikit_property":
            xml_node_name = "cell_volume"
        name_selec_elem = tree.find(xml_node_name)
        if name_selec_elem is None:
            name_selec_elem = ET.SubElement(tree, xml_node_name)
        for cell in natural_sort(self.get_keys()):
            cell_t, cell_id, cell_ch = get_object_t_id_ch(cell)
            astec_identifier = str(get_longid(int(cell_t), int(cell_id)))
            new_cell = ET.SubElement(name_selec_elem, 'cell')
            new_cell.set('cell-id', astec_identifier)
            if xml_node_name == "cell_lineage":
                output = []
                if isinstance(self.values[cell], list):
                    for child in self.values[cell]:
                        cell_t_child, cell_id_child, cell_ch_child = get_object_t_id_ch(child)
                        astec_identifier_child = str(get_longid(int(cell_t_child), int(cell_id_child)))
                        output.append(int(astec_identifier_child))
                else:
                    cell_t_child, cell_id_child, cell_ch_child = get_object_t_id_ch(self.values[cell])
                    astec_identifier_child = str(get_longid(int(cell_t_child), int(cell_id_child)))
                    output.append(int(astec_identifier_child))

            elif self.type == "dict" or xml_node_name == "cell_contact_surface":
                for subcell_key in self.values[cell]:
                    subcell_value = self.values[cell][subcell_key]
                    sub_cell_t, sub_cell_id, sub_cell_ch = get_object_t_id_ch(subcell_key)
                    sub_astec_identifier = str(get_longid(int(sub_cell_t), int(sub_cell_id)))
                    sub_new_cell = ET.SubElement(new_cell, 'cell')
                    sub_new_cell.set('cell-id', sub_astec_identifier)
                    sub_new_cell.text = str(subcell_value)
                continue # no need to write new_cell.text with dict properties
            elif self.type == "string":
                if isinstance(self.values[cell], list):
                    output = []
                    for child in self.values[cell]:
                        output.append(str(child))
                else:
                    output = "'" + str(self.values[cell]) + "'"
            else:
                if isinstance(self.values[cell], list):
                    output = []
                    for child in self.values[cell]:
                        output.append(child)
                else:
                    output = self.values[cell]
            new_cell.text = str(output)

    def generate_txt(self, added_comments=None):
        """
        Generate the txt version of the property, adding comments from added_comments

        :param added_comments: Added comments, list of strings, optional
        :type added_comments: list
        :return: txt version of the property, as a list of line
        :rtype: list of str
        """

        lines = []
        lines.append("#MorphoPlot" + "\n")
        if added_comments is not None:
            for comment in added_comments:
                lines.append("#" + comment + "\n")
        lines.append("type:" + str(self.type) + "\n")
        for idc in natural_sort(self.get_keys()):
            if "cell_contact_surface" in self.name or self.type == "dict":
                for sub_cell_key in self.values[idc]:
                    sub_cell_value = self.values[idc][sub_cell_key]
                    lines.append(str(idc) + ":" + str(sub_cell_key) + ":"+str(sub_cell_value) + "\n")
            else:
                if isinstance(self.values[idc], list):
                    for value in self.values[idc]:
                        lines.append(str(idc) + ":" + str(value) + "\n")
                else:
                    lines.append(str(idc) + ":" + str(self.values[idc]) + "\n")
        return lines

    def clean_at(self, time):
        """
        Remove all elements from the property at time point given in parameter. Used to update scikit properties

        :param time: Time point to remove
        :type time: int
        """
        for object_name in list(self.get_keys()):
            tc, idc, ch = get_object_t_id_ch(object_name)
            if int(tc) == int(time):
                del self.values[object_name]

    def get_object_ids_at(self, time):
        """
        Retrieve the list of object ids in the property for a given time point.

        :param time: Time point to list
        :type time: int
        :return: List of object ids in the property
        :rtype: list

        """
        return [x for x in self.get_keys() if
                int(get_object_t_id_ch(x)[0]) == time and self.values[x] is not None and self.values[x] != ""]

    def get_values_at(self, time=-1):
        """
        Retrieve the list of values in the property for a given time point.
        :param time: Time point to list
        :type time: int
        :return: List of values in the property
        :rtype: list
        """
        if time == -1:
            return self.get_values()
        cell_ids = self.get_object_ids_at(time)
        return [self.values[x] for x in cell_ids]

    def get_float_values_at(self, time=-1):
        """
        Retrieve the list of values in the property for a given time point.
        :param time: Time point to list
        :type time: int
        :return: List of values in the property
        :rtype: list
        """
        if time == -1:
            return [float(x) for x in self.get_values()]
        cell_ids = self.get_object_ids_at(time)
        return [float(self.values[x]) for x in cell_ids]
