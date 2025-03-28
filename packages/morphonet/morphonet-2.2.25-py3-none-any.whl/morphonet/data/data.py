from morphonet.data.dataset import DatasetAnalysis,Image
from morphonet.data import default_parameters
from os.path import join,exists
from os import sep
import json
from morphonet.tools import retrieve_all_temp_folder

def _get_json_file_path():
    local_file_paths = retrieve_all_temp_folder()
    for local_file in local_file_paths:
        local_file_path = join(local_file,"local_datasets-2-2-3.json") #json path is different depending on the os
        if not exists(local_file_path):
            local_file_path = join(local_file,"local_datasets-2-1-17.json") #json path is different depending on the os
        #print("trying : "+local_file_path)
        if exists(local_file_path):
            #print(" found path : "+str(local_file_path))
            return local_file_path
    return ""

def _load_json_file(json_path_override=None):
    local_file_path = json_path_override
    if json_path_override is None:
        local_file_path = _get_json_file_path()
    dataset_list = []
    if local_file_path != "":
        with open(local_file_path, "rb") as jf:
            dataset_json = json.loads(jf.read())
            if "LocalDatasetItems" in dataset_json:
                dataset_list = dataset_json["LocalDatasetItems"]
    return dataset_list

def _return_attribute_if_exist(json_dict, attribute_name):
    # try to find the property in a json dict, and returns it if found.
    # returns None if not
    if not attribute_name in json_dict:
        print("Error : dataset json file does not contain "+attribute_name)
        return None
    return json_dict[attribute_name]

def _parse_dataset(dataset_json,override_temp_path=None):
    # parse a dataset json file. All optional key are swapped if they are absent
    # returns the Dataset object
    name =  _return_attribute_if_exist(dataset_json, "Name") # this function check if key exist, returning none or the property
    if name is None:
        return
    min_time = _return_attribute_if_exist(dataset_json, "MinTime")
    if min_time is None:
        return
    max_time = _return_attribute_if_exist(dataset_json, "MaxTime")
    if max_time is None:
        return
    background = _return_attribute_if_exist(dataset_json, "Background")
    if background is None:
        return
    temp_path = _return_attribute_if_exist(dataset_json, "FullPath")
    if temp_path is None:
        return
    segmented_images = _return_attribute_if_exist(dataset_json, "SegmentedData")
    if segmented_images is None:
       return
    raw_images = _return_attribute_if_exist(dataset_json, "IntensityData")
    if raw_images is None:
        return
    xml_path = _return_attribute_if_exist(dataset_json, "XMLFile")
    if xml_path is None:
        xml_path = ""
    creation_date = _return_attribute_if_exist(dataset_json, "Date")
    if creation_date is None:
        creation_date = ""
    downscale = _return_attribute_if_exist(dataset_json, "DownScale")
    if downscale is None:
        downscale = default_parameters.SEG_DOWNSCALE
    z_downscale = _return_attribute_if_exist(dataset_json, "ZDownScale")
    if z_downscale is None:
        z_downscale = default_parameters.SEG_Z_DOWNSCALE
    raw_downscale = _return_attribute_if_exist(dataset_json, "RawDownScale")
    if raw_downscale is None:
        raw_downscale = default_parameters.RAW_DOWNSCALE
    z_raw_downscale = _return_attribute_if_exist(dataset_json, "ZRawDownScale")
    if z_raw_downscale is None:
        z_raw_downscale = default_parameters.RAW_Z_DOWNSCALE
    smoothing = _return_attribute_if_exist(dataset_json, "Smoothing")
    if smoothing is None:
        smoothing = default_parameters.APPLY_SMOOTHING
    smoothing_passband = _return_attribute_if_exist(dataset_json, "SmoothPassband")
    if smoothing_passband is None:
        smoothing_passband = default_parameters.SMOOTHING_PASSBAND
    smoothing_iterations = _return_attribute_if_exist(dataset_json, "SmoothIterations")
    if smoothing_iterations is None:
        smoothing_iterations = default_parameters.SMOOTHING_ITERATIONS
    quadratic_clustering = _return_attribute_if_exist(dataset_json, "QuadricClustering")
    if quadratic_clustering is None:
        quadratic_clustering = default_parameters.QUADRATIC_CLUSTERING
    quadratic_clustering_divisions = _return_attribute_if_exist(dataset_json, "QCDivisions")
    if quadratic_clustering_divisions is None:
        quadratic_clustering_divisions = default_parameters.QUADRATIC_CLUSTERING_DIVISIONS
    decimation = _return_attribute_if_exist(dataset_json, "Decimation")
    if decimation is None:
        decimation = default_parameters.DECIMATION
    decimation_reduction = _return_attribute_if_exist(dataset_json, "DecimateReduction")
    if decimation_reduction is None:
        decimation_reduction = default_parameters.DECIMATION_REDUCTION
    automatic_decimate_threshold = _return_attribute_if_exist(dataset_json, "AutoDecimateThreshold")
    if automatic_decimate_threshold is None:
        automatic_decimate_threshold = default_parameters.AUTOMATIC_DECIMATION_THRESHOLD
    new_temp_path = temp_path
    if override_temp_path is not None:
        if "\\" in temp_path:
            folder_name = temp_path.split("\\")[-1]
        else:
            folder_name = temp_path.split(sep)[-1]
        new_temp_path = join(override_temp_path,folder_name)
    list_segmentation_images = []
    list_intensities_images = []
    for time_key in segmented_images.keys():
        for channel_Key in segmented_images[time_key].keys():
            image_name = segmented_images[time_key][channel_Key]["Name"]
            image_original_time = segmented_images[time_key][channel_Key]["OriginalTime"]
            image_original_channel = segmented_images[time_key][channel_Key]["OriginalChannel"]
            image_time = segmented_images[time_key][channel_Key]["Time"]
            image_channel = segmented_images[time_key][channel_Key]["Channel"]
            image_path = segmented_images[time_key][channel_Key]["Path"]
            image_voxel_size = segmented_images[time_key][channel_Key]["VoxelSize"]
            image_size = segmented_images[time_key][channel_Key]["Size"]
            image_encoding = segmented_images[time_key][channel_Key]["Encoding"]
            image_object = Image(image_channel,image_time,image_name,image_original_channel,image_original_time,image_path,image_voxel_size,image_size,image_encoding,"",None)
            list_segmentation_images.append(image_object)
    for time_key in raw_images.keys():
        for channel_Key in raw_images[time_key].keys():
            image_name = raw_images[time_key][channel_Key]["Name"]
            image_original_time = raw_images[time_key][channel_Key]["OriginalTime"]
            image_original_channel = raw_images[time_key][channel_Key]["OriginalChannel"]
            image_time = raw_images[time_key][channel_Key]["Time"]
            image_channel = raw_images[time_key][channel_Key]["Channel"]
            image_path = raw_images[time_key][channel_Key]["Path"]
            image_voxel_size = raw_images[time_key][channel_Key]["VoxelSize"]
            image_size = raw_images[time_key][channel_Key]["Size"]
            image_encoding = raw_images[time_key][channel_Key]["Encoding"]
            image_object = Image(image_channel,image_time,image_name,image_original_channel,image_original_time,image_path,image_voxel_size,image_size,image_encoding,"",None)
            list_intensities_images.append(image_object)
    dataset_object = DatasetAnalysis(name,min_time,max_time,background,list_segmentation_images,list_intensities_images,xml_path,creation_date,new_temp_path,downscale,z_downscale,raw_downscale,z_raw_downscale,smoothing,smoothing_passband,smoothing_iterations,quadratic_clustering,quadratic_clustering_divisions,decimation,decimation_reduction,automatic_decimate_threshold)
    return dataset_object


def list_local_datasets(json_override=None):
    """
    Read the local datasets JSON file, and list all the dataset names

    :param json_override: If set, allow to give the code a different JSON local dataset file path than the main morphonet one
    :type json_override: str
    :return: names of the local datasets in MorphoNet TEMP files
    :rtype: list of str
    """
    dataset_names = []
    dataset_json_list = _load_json_file(json_override)
    for dataset_json in dataset_json_list:
        if "Name" in dataset_json:
            dataset_names.append(dataset_json["Name"])
    return list(sorted(dataset_names))


def get_local_dataset(dataset_name,json_override=None,temp_path_override=None):
    """
    Read the local datasets JSON file and return the dataset object for a given name (accepts case mismatch)

    :param dataset_name: name of the dataset to find
    :type dataset_name: str
    :param json_override: optional, provides the path to json file, instead of using the automatic computation of the path
    :type json_override: str
    :param temp_path_override: optional, provides the path to the temp folder, instead of using the normal MorphoNet one. Includes .TEMP folder
    :type temp_path_override: str
    :return: dataset object corresponding to given name
    :rtype: Dataset
    """
    dataset_json_list = _load_json_file(json_override)
    dataset_object = None
    for dataset_json in dataset_json_list:
        if "Name" in dataset_json and dataset_json["Name"].lower() == dataset_name.lower():
            dataset_object = _parse_dataset(dataset_json,temp_path_override)
            break
    return dataset_object
