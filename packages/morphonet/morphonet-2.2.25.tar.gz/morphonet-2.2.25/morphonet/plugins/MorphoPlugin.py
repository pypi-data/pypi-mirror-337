# -*- coding: latin-1 -*-
from os.path import join, isfile

import numpy as np
from datetime import datetime
from morphonet.tools import imread, imsave_thread, printv
import os
import PIL.Image as Image



class MorphoPlugin:
    """Plugin class to be heritate in order to create plugin in MorphoNet  

    Examples
    --------
    >>> class MyFirstPLugin(MorphoPlugin):
    >>>     def __init__(self): 
    >>>         MorphoPlugin.__init__(self) 
    >>>         self.set_name("My First Plugin ")

    """

    def __init__(self):
        self.name = "default plugin name"
        self.description = "default plugin description"
        self.parent = "None"
        self.inputfields = {}
        self.filepickers = {}
        self.filesavers = {}
        self.dropdowns = {}
        self.toggles = {}
        self.dropdowns_sel = {}
        self.icon_name = ""
        self.image_name = ""
        self.coordinates = {}
        self.exec_time = None  # Time of Execution
        self.dataset = None
        self.explanation = None
        self.icon = None
        self.backup = True

    def set_name(self, text_name):  # PLUGIN NAME
        """Define the plugin name

        Parameters
        ----------
        name : string
            the plugin name

        Examples
        --------
        >>> mc.set_name("My first Plugin")
        """
        self.name = text_name
        # Load Explanation
        from importlib_resources import files
        from io import BytesIO
        try:
            im = files("morphonet.plugins").joinpath(join("icons", self.icon_name)).read_bytes()
            self.icon_bytes = im
            self.icon = np.array(Image.open(BytesIO(im)))
        except Exception:
            pass

        try:
            im = files("morphonet.plugins").joinpath(join("images", self.image_name)).read_bytes()
            self.explanation_bytes = im
            self.explanation = np.array(Image.open(BytesIO(im)))
        except Exception as e:
            pass

    def set_description(self, text_description):
        """Define the description of a plugin in order to display it in the MorphoNet Window

        Parameters
        ----------
        text_description : string
            the descrption

        Examples
        --------
        >>> self.set_description("The plugin description ")
        """
        self.description = text_description

    def set_icon_name(self, icon_name):
        """Define the name of the icon to be found in the icons folder to displayit on MorphoNet window

        Parameters
        ----------
        icon_name : string
            the icon name

        Examples
        --------
        >>> self.set_icon_name("plugin_name.png")
        """
        self.icon_name = icon_name

    def set_image_name(self, image_name):
        """Define the name of the images to be found in the image folder to display it on MorphoNet window

        Parameters
        ----------
        image_name : string
            the image name

        Examples
        --------
        >>> self.set_image_name("plugin_name.png")
        """
        self.image_name = image_name

    def set_parent(self, text_name):  # PARENT GROUP
        """Define the parent name in order to group plugin the in the MorphoNet Window

        Parameters
        ----------
        name : string
            the parent name

        Examples
        --------
        >>> self.set_parent("Create new objects")
        """

        self.parent = text_name

    # INPUT FIELD IN UNITY
    def add_inputfield(self, text_name, default=None):
        """Define a new variable for the plugin wich will appear as an Input Field in the Morphow Window

        Parameters
        ----------
        text_name : string
            the name of the variable 
        default_value : multi-type (optional)
            the default value of the variable

        Examples
        --------
        >>> self.add_inputfield("gaussian_sigma",8)
        """
        self._set_inputfield(text_name, default)

    def _set_inputfield(self, text_name, value):
        self.inputfields[text_name] = value

    def get_inputfield(self, text_name):
        """Return the value of the variable in the Input Field in the Morphow Window

        Parameters
        ----------
        text_name : string
            the name of the variable 

        Examples
        --------
        >>> gauss=int(self.get_inputfield("Min gaussian_sigma"))
        """

        return self.inputfields[text_name]

    # FILE PICKER IN UNITY
    def add_filepicker(self, text_name, default=None,Optional=False):
        """Define a new variable for the plugin wich will be appear as a filepicker in the Morphow Window

        Parameters
        ----------
        text_name : string
            the name of the variable
        default_value : multi-type (optional)
            the default value of the variable

        Examples
        --------
        >>> self.add_filepicker("gaussian_sigma",8)
        """
        self.filepickers[text_name] = {'value': default, 'Optional':Optional}

    def _set_filepicker(self, text_name, value):
        self.filepickers[text_name]['value'] = value

    def get_filepicker(self, text_name):
        """Return the value of the variable in the picker Input Field in the Morphow Window

        Parameters
        ----------
        text_name : string
            the name of the variable

        Examples
        --------
        >>> filename=self.get_filepicker("pick a file")
        """
        return self.filepickers[text_name]['value']

    # FILE SAVER IN UNITY
    def add_filesaver(self, text_name, default=None):
        """Define a new variable for the plugin wich will appear as a filepicker in the Morphow Window

        Parameters
        ----------
        text_name : string
            the name of the variable
        default_value : multi-type (optional)
            the default value of the variable

        Examples
        --------
        >>> self.add_filesaver("save to","my/path/filename.txt")
        """
        self._set_filesaver(text_name, default)

    def _set_filesaver(self, text_name, value):
        self.filesavers[text_name] = value

    def get_filesaver(self, text_name):
        """Return the value of the variable in the saver Input Field in the Morphow Window

        Parameters
        ----------
        text_name : string
            the name of the variable

        Examples
        --------
        >>> filename=self.get_filesaver("save to")
        """
        return self.filesavers[text_name]

    # DROWDOWN IN UNITY
    def add_dropdown(self, text_name, option):
        """Define a new variable as a list of options for the plugin wich will be appear as a Dropdown in the Morphow Window

        Parameters
        ----------
        text_name : string
            the name of the variable 
        option : list of string 
            list of options 

        Examples
        --------
        >>> self.add_dropdown("Inverse",["no","yes"])
        """

        self.dropdowns[text_name] = option
        self._set_dropdown(text_name, 0)

    def _set_dropdown(self, text_name, value):
        self.dropdowns_sel[text_name] = int(value)

    def get_dropdown(self, text_name):
        """Return the value of the variable enter in the Dropdown in the Morphow Window

        Parameters
        ----------
        text_name : string
            the name of the variable 

        Examples
        --------
        >>> isOk=self.get_dropdown("Inverse")=="yes"
        """
        return self.dropdowns[text_name][self.dropdowns_sel[text_name]]

    # TOGGLES IN UNITY
    def add_toggle(self, text_name, default=True):
        self._set_toggle(text_name, default)

    def _set_toggle(self, text_name, value):
        self.toggles[text_name] = value

    def get_toggle(self, text_name):
        if text_name in self.toggles:
            return self.toggles[text_name]
        return None

    # ADD COORDINATES IN UNITY
    def add_coordinates(self, text_name):
        """Define a new variable as a list of 3D coordinates wich allow you the get the list of corrdinates entered in the Morphow Window

        Parameters
        ----------
        text_name : string
            the name of the variable 

        Examples
        --------
        >>> self.add_coordinates("seeds")
        """
        self.coordinates[text_name] = []

    def _set_coordinates(self, text_name, coords):  # Recieve '(-0.9, 0.2, -3.5); (0.1, -0.2, -3.5); (0.9, -0.6, -3.5)'
        if coords != "":
            self.coordinates[text_name] = []
            for s in coords.split(";"):
                self.coordinates[text_name].append(np.float32(s[1:-1].split(',')))

    def get_coordinates(self, text_name):
        """Return the list of coordinates defined in the Morphow Window

        Parameters
        ----------
        text_name : string
            the name of the variable 

        Examples
        --------
        >>> seeds=self.get_coordinates("seeds")
        """

        return self.coordinates[text_name]

    # INTERNAL COMMAND
    def _cmd(self):
        return self.name

    def _get_btn(self):
        c = self._cmd() + ";" + self.parent
        for tf in self.inputfields:
            c += ";IF_" + str(tf)
            if self.inputfields[tf] is not None:
                c += ";DF_" + str(self.inputfields[tf])
        for fp in self.filepickers:
            c += ";FP_" + str(fp)
        for fs in self.filesavers:
            c += ";FS_" + str(fs)
        for dd in self.dropdowns:
            c += ";DD_" + str(dd) + "_"
            for v in self.dropdowns[dd]:
                c += str(v) + "_"
        for cd in self.coordinates:
            c += ";CD_" + str(cd)
        for cb in self.toggles:
            c += ";CB_" + str(cb) + "_" + str(self.toggles[cb])
        # DO NOT HIDE SE or PR as shortcuts (already used)
        return c

    # Start the plugin
    def start(self, t, dataset, objects, objects_require=True, backup=True):
        """Start function which have be to be exectuted at the begining of the process 

        Parameters
        ----------
        t : time
            the specitic time step on the MorphoNet Window
        dataset: dataset
            the dataset variable
        objects :
            the selected objects int the MorphoNet Window
        backup: Do we need to backup something ?
            False only when we don't modify anything (seeds creation for example)

        Examples
        --------
        >>>     def process(self,t,dataset,objects): #PLUGIN EXECUTION
        >>>         if not self.start(t,dataset,objects): 
        >>>             return None

        """

        self.exec_time = datetime.now()
        self.dataset = dataset
        self.t = t
        self.objects = objects
        printv("Process " + self.name, 0)
        isOk = True
        for tf in self.inputfields:
            if self.inputfields[tf] is None or self.inputfields[tf] == "":
                printv("Please fill the parameter " + str(tf), 0)
                isOk = False
            else:
                printv("Found " + str(tf) + " = " + str(self.inputfields[tf]), 0)

        for fp in self.filepickers:
            if self.filepickers[fp]['value'] is None or self.filepickers[fp]['value'] == "":
                if not self.filepickers[fp]['Optional']:
                    printv("Please fill the parameter " + str(fp), 0)
                    isOk = False
            else:
                printv("Found " + str(fp) + " = " + str(self.filepickers[fp]['value']), 0)
        for fs in self.filesavers:
            if self.filesavers[fs] is None or self.filesavers[fs] == "":
                printv("Please fill the parameter " + str(fs), 0)
                isOk = False
            else:
                printv("Found " + str(fs) + " = " + str(self.filesavers[fs]), 0)

        for cb in self.toggles:
            printv("Found " + str(cb) + " = " + str(self.toggles[cb]), 0)

        if objects_require:
            if len(self.objects) == 1 and self.objects[0] == '' or len(self.objects) == 0 or self.objects is None:
                printv("Please select first something before running " + self.name, 0)
                isOk = False

        if isOk and backup:
            dataset.start_step(self.get_log(), self.exec_time)

        if not isOk:
            self.dataset.restart(self)
        return isOk

    def get_log(self):
        log = "Plugin:" + self.name + "(" + self.parent + "); Time:" + str(self.t) + ";"
        for tf in self.inputfields:
            log += " IF:" + str(tf) + ":" + str(self.get_inputfield(tf)) + ";"
        for fp in self.filepickers:
            log += " FP:" + str(fp) + ":" + str(self.get_filepicker(fp)) + ";"
        for fs in self.filesavers:
            log += " FS:" + str(fs) + ":" + str(self.get_filesaver(fs)) + ";"
        for dd in self.dropdowns:
            log += " DD:" + str(dd) + ":" + str(self.get_dropdown(dd)) + ";"
        for cd in self.coordinates:
            log += " CD:" + str(cd) + ":" + str(self.get_coordinates(cd)) + ";"
        for cb in self.toggles:
            log += " CB:" + str(cb) + ":" + str(self.get_toggle(cb)) + ";"
        if self.objects is not None and len(self.objects) > 0 and self.objects[0] != '':
            log += " ID:" + str(self.objects) + ";"
        # DO NOT HIDE SE or PR as shortcuts (already used)
        return log

    # Restart the curation
    def restart(self, cancel=False, label=None):
        """Restart function which have be to be exectuted at the end of the process in order to restart properlly the curation

        Examples
        --------
        >>>     def process(self,t,dataset,objects):
        >>>         if not self.start(t,dataset,objects):
        >>>             return None
        >>>         ...
        >>>         ... plugin execution  ...
        >>>         ...
        >>>         self.restart()

        """

        if cancel:
            self.dataset.cancel()
        elif self.backup:
            self.dataset.end_step()
        self.dataset.restart(self, label=label)

    #filter out the labels in objects parameter that are not in the dataset
    def filter_objects(self,objects, dataset):
        if dataset is None:
            return None
        real_objects = []
        i = 0
        if len(objects) > 0 and objects[0] != "":
            for o in dataset.get_objects(objects):
                if dataset.get_regionprop("bbox",o) is not None:
                    real_objects.append(objects[i])
                i += 1
        return real_objects



    # IMAGE PROCESSING FUNCTIONS
    def gaussian_rawdata(self, t, sigma=2, preserve_range=True):
        from skimage.filters import gaussian
        rawdata = self.dataset.get_raw(t)
        if sigma <= 0:
            return rawdata

        printv("Perform gaussian with sigma=" + str(sigma), 0)
        gauss_file = join(self.dataset.parent.temp_path, "rawdata_" + str(t) + "_gauss_" + str(sigma) + ".tiff")
        if isfile(gauss_file):
            gauss_data = imread(gauss_file)[:, :, :, 0, 0]
            return gauss_data
        rawdata = gaussian(rawdata, sigma=sigma, preserve_range=preserve_range)
        sst = imsave_thread(gauss_file, rawdata)
        sst.start()
        return rawdata
