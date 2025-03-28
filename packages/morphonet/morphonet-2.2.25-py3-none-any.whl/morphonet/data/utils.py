from morphonet.tools import get_id_t,_set_dictionary_value,get_property_type
import xml.etree.ElementTree as ET
import os
from datetime import datetime



def generate_prop_naming_parameters(xml_folder, xml_file,atlas_path):
    """ Generate the parameter file used by ASCIDIANS to propagate naming in a property file, and save it to disk


    :param xml_folder: folder containing the property file
    :type xml_folder: str
    :param xml_file: name of the file in the XML folder
    :type xml_file: str
    :param atlas_path: list of properties file paths to use for naming template atlas
    :type atlas_path: list
    :returns: The path to the property file
    :rtype: str
    """
    atlases_files = []
    now = datetime.now()
    parameters_name = "prop_naming" + str(now.timestamp()).replace('.', '') + ".py"
    txt = ""
    final_file = os.path.join(xml_folder, xml_file)
    txt += "inputFile = '" + str(final_file) + "'" + "\n"
    txt += "outputFile = '" + str(final_file) + "'" + "\n"
    txt += "confidence_atlases_nmin = 2" + "\n"
    txt += "write_selection = False" + "\n"
    txt += "confidence_atlases_percentage = 0" + "\n"
    txt += 'atlasFiles = ' + str(atlas_path) + "\n"
    atlases_files.append("pm9.xml")
    f = open(parameters_name, "w+")
    f.write(txt)
    f.close()
    return parameters_name

def generate_init_naming_parameters(begin_cell_count, xml_folder, xml_file,atlas_path):
    """ Generate the parameter files needed for ASCIDIANS initial naming.


    :param begin_cell_count: Number of cells for starting time point
    :type begin_cell_count: int
    :param xml_folder: Folder containing property files to name
    :type xml_folder: str
    :param xml_file: Name of the property file to use for naming
    :type xml_file: str
    :param atlas_path: list of properties file paths to use for naming template atlas
    :type atlas_path: list

    :returns: path to the parameter file created
    :rtype: str
    """
    now = datetime.now()
    parameters_name = "init_naming" + str(now.timestamp()).replace('.', '') + ".py"
    final_file = os.path.join(xml_folder, xml_file)
    txt = ""
    txt += "inputFile = '" + str(final_file) + "'" + "\n"
    txt += "outputFile = '" + str(final_file) + "'" + "\n"
    txt += "cell_number = " + str(begin_cell_count) + "\n"
    txt += 'atlasFiles = ' + str(atlas_path) + "\n"
    txt += "check_volume=False" + "\n"
    f = open(parameters_name, "w+")
    f.write(txt)
    f.close()
    return parameters_name

def remove_folder(path):
    """
    Empty the folder given in parameter, and delete it

    :param path: path to the folder to remove
    :type path: str
    """
    import os
    import shutil
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)  # remove dir and all contains
    else:
        raise ValueError("file {} is not a file or dir.".format(path))

def indent_xml(elem, level=0):
    """ Recursively auto indent a XML object to save it to file

    :param elem: XML object to be indented
    :type elem: xml.etree.ElementTree.Element
    :param level: Level of indentation (Default value = 0)
    :type level: int
    :return: Indented XML object
    :rtype: xml.etree.ElementTree.Element

    """
    i = "\n" + level*"  "
    j = "\n" + (level-1)*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent_xml(subelem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j
    return elem


def get_object_id(t,idc,ch=0):
    """
    Returns the object key used in properties from the cell t, id and channel
    :param t: time point of the object
    :type t: int
    :param idc: object identifier in segmentation
    :type idc: int
    :param ch: channel number (optional, default = 0)
    :type ch: int
    :return: object key
    :rtype: str
    """
    return str(t)+","+str(idc)+","+str(ch)


def get_object_t_id_ch(object_id):
    """
    Split the object identifier used to store object properties key to access time point, channel and object identifier
    :param object_id: Object if with format t,id,channel
    :type object_id: str
    :return: tuple (t,id,ch)
    :rtype: tuple
    """
    return object_id.split(",")

def load_properties_from_xml(xml_file,seg_channel=0):
    """
    Load all properties from a property file (xml) as MorphoNet.data properties

    :param xml_file: name of the property file to read
    :type xml_file: str
    :param seg_channel: channel number (optional, default = 0)
    :type seg_channel: int
    :return: list of properties
    :rtype: list
    """
    properties = []
    from morphonet.data.dataproperty import DataProperty
    try:
        source = open(xml_file)
    except:
        print("XML file not found")
        return None
    tree = ET.parse(source)
    root = tree.getroot()
    for child in root:
        property_name = child.tag
        prop_type = get_property_type(property_name)
        if property_name == "cell_lineage":
            temporal_property = DataProperty(None, "temporal", "", "time")
            prop = _set_dictionary_value(child)
            for idl in prop:
                tc, idc = get_id_t(idl)
                for daughter in prop[idl]:
                    td, idd = get_id_t(daughter)
                    child_identifier = get_object_id(td, idd, seg_channel)
                    temporal_property.set_object_value(tc,idc, seg_channel, child_identifier)
            properties.append(temporal_property)
        elif property_name == "cell_contact_surface" or prop_type == "dict":
            property_object = DataProperty(None, property_name, "", prop_type)
            prop = _set_dictionary_value(child)
            for idl in prop:
                vals = []
                tc, idc = get_id_t(idl)
                for id_contact in prop[idl]:
                    tconact,idcontact = get_id_t(id_contact)
                    contact_id = get_object_id(tconact, idcontact, seg_channel)
                    property_object.set_object_value(tc, idc,seg_channel, (contact_id,prop[idl][id_contact]))
            properties.append(property_object)
        else:
            prop_type = get_property_type(property_name)
            property_object = DataProperty(None, property_name, "", prop_type)
            prop = _set_dictionary_value(child)
            for idl in prop:
                tc, idc = get_id_t(idl)
                property_object.set_object_value(tc, idc,seg_channel, prop[idl])
            properties.append(property_object)
    return properties

def load_cell_list(path_lineage,lineage_property="cell_lineage",seg_channel=0):
    """ Load the content of "cell_lineage" property from the properties file, as a dict of key being cell keys, value the cell object

    :param path_lineage: Path to the property file
    :type path_lineage: str
    :param lineage_property: Name of the lineage property
    :type lineage_property: str
    :param seg_channel: Channel number (optional, default = 0)
    :type seg_channel: int
    :return: Dict of key being cell keys, value the cell object
    :rtype: dict

    """
    from morphonet.data.dataproperty import DataProperty
    try:
        source = open(path_lineage)
    except:
        print("XML file not found")
        return None
    temporal_property = None
    tree = ET.parse(source)
    root = tree.getroot()
    if root.tag == lineage_property:
        temporal_property = DataProperty(None, "temporal", "", "time")
        prop = _set_dictionary_value(root)
        for idl in prop:
            tc, idc = get_id_t(idl)
            for daughter in prop[idl]:
                td, idd = get_id_t(daughter)
                child_identifier = get_object_id(td,idd,seg_channel)
                temporal_property.set_object_value(tc, idc,seg_channel, child_identifier)
    else:
        for child in root:
            if child.tag == lineage_property:
                temporal_property = DataProperty(None, "temporal", "", "time")
                prop = _set_dictionary_value(child)
                for idl in prop:
                    tc, idc = get_id_t(idl)
                    for daughter in prop[idl]:
                        td, idd = get_id_t(daughter)
                        child_identifier = get_object_id(td,idd,seg_channel)
                        temporal_property.set_object_value(tc,idc, seg_channel, child_identifier)
    return temporal_property

def write_lineage_to_step(dataset,step,lineage_property):
    """ Save a given dictionary to a morphonet text format property. Giving a type to the information is important

    :param step: Step identifier for dataset
    :type path_output: int
    :param name_file: Name of the information and file
    :type name_file: str
    :param property_dict: Dict of key being cell keys, value being value
    :type property_dict: dict
    """
    if lineage_property.type != "time": # lineage property MUST be time
        lineage_property.type = "time"
    dataset.write_property_to_step(step,"temporal.txt",lineage_property)

def get_previous_cell_in_lineage(cell_key,lineage_property):
    """ For a given cell key, provide the mother cell key from the lineage information

    :param cell_key: Cell key to find the mother. Format : t,id,channel (channel being optional)
    :type cell_key: str
    :param lineage_property: Name of the lineage property
    :type lineage_property: MorphoNet.data property
    :return: Mother cell key
    :rtype: str
    """
    if lineage_property is None:
        print("Lineage property is none , unable to get mother cell")
        return None
    for key_tmp in lineage_property.get_keys() :
        if lineage_property.values[key_tmp] is not None and len(lineage_property.values[key_tmp]) > 0:
            for cell in lineage_property.values[key_tmp]:
                if cell == cell_key:
                    return key_tmp
    return None

def get_next_cells_in_lineage(cell_key,lineage_property):
    """ For a given cell key, provide the list of daughter cell keys from the lineage information

    :param cell_key: Cell key to find the mother. Format : t,id,channel (channel being optional)
    :type cell_key: str
    :param lineage_property: Name of the lineage property
    :type lineage_property: MorphoNet.data property
    :return: daughters cell key list
    :rtype: list
    """
    if lineage_property is None:
        print("Lineage property is none , unable to get mother cell")
        return None
    if cell_key in lineage_property.get_keys():
        return lineage_property[cell_key]
    return None

def list_properties_in_pickle(pickle_file):
    """
    Read the pickle file given in parameter, and retrieve all properties found inside by name

    :param pickle_file: Name of the pickle file
    :type pickle_file: str
    :return: List the property names found
    :rtype: list
    """
    import pickle
    names = []
    with open(pickle_file, "rb") as infile:
        prop = pickle.load(infile)
        for cell_id in prop:
            for property_name in prop[cell_id]:
                if not property_name in names:
                    names.append(property_name)
    return names

def get_symetric_cells(timepoint,property,name):
    #print(name)
    for cell_key in property.get_keys():
        tc,idc,channelc = get_object_t_id_ch(cell_key)
        if tc == timepoint:
            sname = property.get_object_value(tc,idc,channelc)
            if sname is not None:
                if sname!=name and sname[0:-1] == name[0:-1]:
                    #print("found symetric "+str(sname))
                    return cell_key
    return None

def get_node(property_lineage,cell_key, shift=1):
    node = [cell_key] #Ids of the dons
    life=[1] #Life lenght
    adj=[] #Lineage relation
    daughters = []
    tc,idc,channelc = get_object_t_id_ch(cell_key)
    if cell_key in property_lineage.get_keys():
        daughters = property_lineage.get_object_value(tc,idc,channelc)
    if len(daughters) == 0:  # [a],[]
        adj= [[]]
    elif len(daughters) == 1:  # [a,b],[[1],[]]
        node, adj ,life= get_node(property_lineage,daughters[0],shift=shift)
        life[0]+=1
        node[0]=cell_key
    else:   # Multiples Daughters (Division)
        final_adj = []
        for d in daughters:
            adj.append(shift)
            d_node, d_adj,d_life = get_node(property_lineage,d,shift=shift)
            node += d_node
            life+=d_life
            for dd in d_adj: final_adj.append(dd)
            shift += len(node) - 1
        adj=[adj] + final_adj
    return node, adj, life  # Correspond to x_node,x_adj, x_life

def get_all_regionprop_names():
    """ Print all computable region property

    """
    return ['area','area_bbox', "bbox",'volume_real', 'volume_filled','convexity',
                                    'axis_major_length', 'axis_minor_length', 'axis_ratio', "diameter",
                                    'equivalent_diameter_area',
                                    'euler_number', 'extent', "connected_neighbors",
                                     'roughness', "compactness", "smoothness",
                                    'intensity_max', 'intensity_mean', 'intensity_min',
                                    'intensity_border_variation', "intensity_offset",
                                    "lineage_distance", 'mother-daughter-ratio']
def is_property_a_regionprop(property_name):
    """
    Test if the given property_name is among the region props possible in MorphoNet

    :param property_name: Name of the property to test (case sensitive)
    :type property_name: str
    :return: True if the property is among the region props possible in MorphoNet
    :rtype: bool
    """
    possible_props = get_all_regionprop_names()
    return property_name in possible_props
