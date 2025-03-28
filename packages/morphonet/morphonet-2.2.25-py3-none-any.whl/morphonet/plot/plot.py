# -*- coding: latin-1 -*-
import os
from http.server import HTTPServer

import numpy as np

from morphonet import tools
from morphonet.plot import ScikitProperty
from morphonet.plot.Dataset import Dataset
from morphonet.plot.Server import  _MorphoServer
from morphonet.tools import isfile, rmrf, rm, printv, convert_vtk_file_in_obj, RemoveLastTokensFromPath, \
    fast_convert_to_OBJ, _check_version, mkdir, convert, apply_mesh_offset, read_mesh, natural_sort, \
    get_tc_from_filename, image_minmax,get_temp_raw_filename_at, _load_seg
from os.path import isdir, join
from hashlib import sha256
from sys import platform, exit
from time import time, strftime, gmtime




class Plot:  # Main function to initalize the plot mode
    """Plot data onto the 3D viewer of the MorphoNet Window.

    Parameters (mostly for debuging )
    ----------
    log : bool
        keep the log
    start_browser : bool
        automatically start the browser when plot initliaze
    port_send : int
        port number to communicate (send messages) with the MorphoNet Window.
    port_send : int
        port number to communicate (receive messages) with the MorphoNet Window.
    temp_folder: string
        Path where MoprphoNet store temporary data (annotation , meshes , etc ..)
    verbose : int
         verbose of the terminal (0 : nothing , 1 : normal user, 2 : develloper)

    Returns
    -------
    MorphoPlot
        return an object of morphonet which will allow you to send data to the MorphoNet Window.


    Examples
    --------
    >>> import morphonet
    >>> mn=morphonet.Plot()

    """

    def __init__(self, log=True, start_browser=False, port_send=9875, port_recieve=9876, memory=20,temp_folder=".TEMP",full_path=False,verbose=1,start_servers=True,check_version=True):
        #global verb
        self.full_path = full_path
        self.temp_folder = temp_folder
        self.memory=memory
        self.start_servers = start_servers
        if self.start_servers:
            self.setup_plot(port_send=port_send,port_recieve=port_recieve,start_browser=start_browser,check_version=check_version)
        self.start_plot(log)
        tools.verbose=verbose
        tools.plot_instance=self
        self.conversion_raw = False  # True when the RAW conversion is done
        self.conversion_meshes=False #True wen the meshes conversion is done
        self.show_raw=False #The Menu of RAw is not yet open
        self.show_raw_t=-1
        self.set_mesh_parameters() #set default mesh parameters in base
        self.recompute = False
        self.uploading = False
        #other init
        self.factor = 1  # Reduce factor to compute the obj
        self.z_factor = 1
        self.raw_factor = 1  # Reduction factor
        self.z_raw_factor = 1  # Reduction factor
        self.current_time = 0

        #optional mesh params
        self.smoothing = True
        self.smooth_passband = 0.01
        self.smooth_iterations = 25
        self.quadric_clustering = True
        self.qc_divisions = 1
        self.decimation = True
        self.decimate_reduction = 0.8
        self.auto_decimate_threshold = 30
        self.voxel_size = (1.0,1.0,1.0)

        self.force_exit = False

    def set_current_time(self,time):
        self.current_time = time

    def setup_plot(self,port_send=9875,port_recieve=9876,start_browser=True,check_version=True):
        if check_version: _check_version()
        #else : get_version()

        self.server_send = _MorphoServer(self, "send", port=port_send)  # Instantiate the local MorphoNet server
        self.server_send.daemon=True
        self.server_send.start()

        self.server_recieve = _MorphoServer(self, "recieve", port=port_recieve)  # Instantiate the local MorphoNet server
        self.server_recieve.daemon=True
        self.server_recieve.start()

        if start_browser:
            self.show_browser() #Open Firefox

    def wait_for_servers(self):
        if self.server_send is not None:
            self.server_send.join()
        if self.server_recieve is not None:
            self.server_recieve.join()
        self.check_exit()

    def start_plot(self,log=True):
        '''
        Initialize MorphoPlot session
        '''
        self.plugins = []
        self.log = log

    def restart_plot(self):
        '''
        Restart MorphoPlot session
        '''
        if self.dataset is not None:
            printv("Restarting  morphoplot session",1)
            self.start_plot(self.log)
            begin = self.dataset.begin
            self.set_current_time(self.dataset.begin)
            end = self.dataset.end
            raw_path = self.dataset.raw_path
            segment = self.dataset.segment
            raw_data = self.dataset.raw_dict
            log = self.dataset.log
            background = self.dataset.background
            xml_file = self.dataset.xml_file
            del self.dataset
            self.set_dataset(begin=begin,end=end,raw=raw_path,segment=segment,background=background,xml_file=xml_file)
            self.curate()

    def connect(self, login, passwd):  # Need to be connected to be upload on MorphoNet
        """Connect to the MorphoNet server

        In order to directly upload data to the MorphoNet server, you have to enter your MorphoNet credentials

        Parameters
        ----------
        login : string
            your login in MorphoNet
        passwd : string
            your password in MorphoNet

        Examples
        --------
        >>> import morphonet
        >>> mc=morphonet.Plot()
        >>> mc.connect("mylogin","mypassword")
        """
        import morphonet
        self.mn = morphonet.Net(login, passwd)

    def send(self, cmd, obj=None):
        """ Send a command to the 3D viewer

        Examples
        --------
        mc.send("hello")
        """
        self.server_send.add(cmd,obj)

    def quit(self):
        """ Stop communication between the browser 3D viewer and python

        Examples
        --------
        mc.quit()
        """
        self.send("MSG","DONE")
        self.server_send.stop()  # Shut down the server
        self.server_recieve.stop()  # Shut down the server

    def quit_and_exit(self):
        """ Stop communication between the browser 3D viewer and python, than exit curation

        Examples
        --------
        mc.quit_and_exit()
        """
        self.send("MSG","DONE_AND_EXIT")
        self.server_send.stop()  # Shut down the server
        self.server_recieve.stop()  # Shut down the server
        exit()

    def upload(self, dataname, net_instance=None, raw_factor=4,raw_z_factor=4):
        """Create the dataset on MorphoNet server and upload data

        Parameters
        ----------
        dataname : string
            Name of the new dataset on the server
        net_instance : morphonet.Net
            Instanciated net object with connected user
        raw_factor : float
            the scaling attached to the dataset to match the raw data
        raw_z_factor : float
            the scaling attached to the dataset to match the raw data for z axis

        Examples
        --------
        >>> ...after starting MorphoPlot and curating the data
        >>> mc.upload("new dataset name",1)
        """
        self.uploading = True
        printv("Upload dataset " + dataname,1)
        net = None
        if net_instance is not None:
            net = net_instance
        else:
            net = self.mn
        self.dataset.init_channels()
        self.dataset.init_raw()

        net.create_dataset(dataname, minTime=self.dataset.begin, maxTime=self.dataset.end)
        center=None
        voxel_size=None
        for t in range(self.dataset.begin, self.dataset.end + 1):
            for c in self.dataset.segmented_channels:
                # compute voxel_size from seg
                #self.dataset.compute_voxel_size_from_seg(t,c)
                obj = self.compute_mesh(t,c)
                if voxel_size is None and self.dataset.seg_dict is not None:
                    voxel_size = self.dataset.seg_dict[str(t)][str(c)]["VoxelSize"]
                if center is None and voxel_size is not None:
                    center = [self.dataset.get_center()[0]*voxel_size[0], self.dataset.get_center()[1]*voxel_size[1],
                          self.dataset.get_center()[2]*voxel_size[2]]

                cobj = apply_mesh_offset(obj, center)
                net.upload_mesh_at(t,cobj,channel=c)

            if t in self.dataset.nb_raw_channels:
                for c in range(self.dataset.nb_raw_channels[t]):
                    raw = self.dataset.get_raw(t,c)
                    if voxel_size is None and self.dataset.raw_dict is not None:
                        voxel_size = self.dataset.raw_dict[str(t)][str(c)]["VoxelSize"]
                    if raw is not None:
                        data8 = convert(raw, 255, np.uint8)
                        if raw_factor > 1 or raw_z_factor > 1:
                            data8 = data8[::raw_factor, ::raw_factor, ::raw_z_factor]

                        if raw_factor != raw_z_factor:
                            voxel_size[2] = voxel_size[2]/(raw_factor/raw_z_factor)

                        vs="{},{},{}".format(voxel_size[0],voxel_size[1],voxel_size[2])
                        scale = raw_factor
                        net.upload_image_at(t,data8,vs,channel=c,scale=scale)

        printv("Uploading done",1)
        self.uploading = False

    def show_browser(self):
        """ Start Mozilla Firefox browser and open morphoplot page

        Examples
        --------
        mc.show_browser()
        """
        import webbrowser
        from morphonet import url
        printv("Open " + url, 1)
        try:
            webbrowser.get('firefox').open_new_tab("http://" + url + '/morphoplot')
        except Exception as e:
            printv("Firefox error: " % e, 1)
            quit()

    def cancel(self):
        '''
        Cancel last action -> retrieve last backup
        '''
        self.dataset.cancel()

    def cancel_to_visualization_step(self):
        '''
        Cancel all last actions until we match current visualization step
        '''
        self.dataset.cancel_to_visualization_step()

    def send_actions(self):
        '''
        Send To Unity the list of actions
        '''
        actions = self.dataset.get_actions()
        self.send("ACTIONS",actions)

    def check_exit(self):
        """

        Checks if plot instance should exit.
        -------

        """
        if self.force_exit:
            exit(0)

    def curate(self, load_default_plugins=True):  # START UPLOAD AND WAIT FOR ANNOTATION
        """ Start sending data to the browser 3D viewer, then wait for annotation from the browser

        Examples
        --------
        mc=morphonet.Plot(start_browser=False)
        mc.set_dataset(...)
        mc.curate()
        """
        start_time = time()
        self.set_current_time(self.dataset.begin)  # Initialise current time point at the first one
        printv("Wait for the MorphoNet Window", 1)
        self.send("START_" + str(self.dataset.begin) + "_" + str(self.dataset.end))  # if curation on , restart_plot
        if load_default_plugins: self.set_default_plugins()  # Initialise Default set of plugins

        # PROPERTIES
        self.plot_properties()
        self.plot_annotations()
        self._reset_properties()
        self.send_properties_name()

        # CHANNELS INITIALSIATION
        self.dataset.init_channels()

        # INITALISE SCIKIT REGION PROPERTIES
        self.send_available_regionprops()  # SEND LIST OF AVAIABLE SCIKIT PROPERTIES

        # RAW IMAGES
        self.dataset.init_raw()  # START RAW CONVERSION

        # MESHES
        self.plot_meshes()
        self.plot_steps_number()

        #PLOT THE RAW DATA
        self.plot_raw(self.dataset.end)  # Launch the Plot if the conversion is ready

        # ACTIONS LIST
        self.send_actions()

        self.plot_stop_loading()

        printv(f"Dataset was created in : {strftime('%H:%M:%S', gmtime(time()-start_time))}",1)

        self.wait_for_servers()

    def restart(self, times, label=None, cancel=False):
        if times is not None:  self.plot_meshes(times)  # PLOT MESHES


        self.plot_steps_number()

        self.plot_raw(self.current_time)  # PLOT RAWDATAS

        self.plot_seeds(self.dataset.get_seeds())  # PLOT SEEDS

        self.dataset.compute_lineage_distance()  # Compute Cell Lineage Distance if asked

        self.delete_properties()  # REMOVE PROPERTIES WHICH HAVE BEEN DELETED

        self.plot_properties(re_read=cancel)  # PLOT ALL PROPERTIES

        self.plot_regionprops()  # PLOT ALL LOADED REGION PROPERTIES

        self.plot_label(label)  # PLOT label

        self.send_actions()  # UPDATE ACTIONS LIST

        self._reset_properties()

        self.plot_stop_loading()



    #########################################  DATASET

    def set_dataset(self, begin=0, end=0, raw=None, segment=None, background=0, xml_file=None,import_temp=False,temp_archive_path="",factor=1,z_factor=1,raw_factor=1,z_raw_factor=1):
        """ Define a dataset

        Parameters
        ----------
        begin : int
            minimal time point
        end : int
            maximal time point
        raw : string
            path to raw data file where time digits are in standard format (ex: {:03d} for 3 digits )(accept .gz)
        segment : string
            path to segmented data file  where time digits are in standard format (ex: {:03d} for 3 digits ) (accept .gz)
        background : int
            the pixel value of the background inside the segmented image
        xml_file : string
            path to the xml propertie files (.xml)
        Examples
        --------
        after connection
        mc.set_dataset(self,begin=0,end=10,raw="path/to/name_t{:03d}.inr.gz",segment="path/to/segmenteddata_t{:03d}.inr.gz",xml_file="path/to/properties_file.xml")
        """
        #default values for image scaling factors
        self.factor = factor  # Reduce factor to compute the obj
        self.z_factor = z_factor
        self.raw_factor = raw_factor  # Reduction factor
        self.z_raw_factor = z_raw_factor  # Reduction factor
        self.current_time = begin
        # Set Temporary folder
        if not self.full_path:
            self.temp_path = ""
            temp_suffix = ""
            if segment is not None or raw is not None:
                if segment is not None and segment != "":
                    temp_suffix = segment
                elif raw is not None and raw != "":
                    temp_suffix = raw

                if platform == "win32" and (
                        '{' in temp_suffix or '}' in temp_suffix or ':' in temp_suffix):  # on windows, create a path without special characters
                    temp_suffix = temp_suffix.replace(":", "")  # .replace(os.sep,'_')

                self.temp_path = str(os.path.basename(temp_suffix))

            #add most params to path
            hcode = int(sha256(temp_suffix.encode('utf-8')).hexdigest(), 16) % 10**8
            self.temp_path += "_"+str(hcode)
            self.temp_path=join(self.temp_folder,self.temp_path)
        else:
            self.temp_path = self.temp_folder
            self.temp_folder = RemoveLastTokensFromPath(self.temp_folder, 1)[:-1]

            if platform == "win32" and '{:' in self.temp_path:  # on windows, create a path without special characters
                self.temp_path = self.temp_path.replace("{:", "").replace("}", "")

        mkdir(self.temp_folder)
        mkdir(self.temp_path)

        if import_temp:
            if os.path.isfile(temp_archive_path) and temp_archive_path.endswith("zip"):
                import shutil
                shutil.unpack_archive(temp_archive_path, self.temp_path, "zip")

        self.show_raw_t = -1  # default: raw to show is the first one

        self.dataset = Dataset(self, begin, end, raw=raw, segment=segment, log=self.log, background=background,
                               xml_file=xml_file, temp_path=self.temp_path)

    def set_dataset_with_dict(self, begin=0, end=0, raw_data=None, segment_data=None, background=0, xml_file=None, import_temp=False,
                    temp_archive_path="", segname=None, factor=1,z_factor=1,raw_factor=1,z_raw_factor=1):
        """ Define a dataset, using dictionaries for data instead of a single string

        Parameters
        ----------
        begin : int
            minimal time point
        end : int
            maximal time point
        raw_data : dict
            path to raw data file where time digits are in standard format (ex: {:03d} for 3 digits )(accept .gz)
        segment_data : dict
            path to segmented data file  where time digits are in standard format (ex: {:03d} for 3 digits ) (accept .gz)
        background : int
            the pixel value of the background inside the segmented image
        xml_file : string
            path to the xml properties files (.xml)

        """
        # default values for image scaling factors
        self.factor = factor
        self.raw_factor = raw_factor
        self.z_raw_factor = z_raw_factor if z_raw_factor is not None else raw_factor
        self.z_factor = z_factor if z_factor is not None else factor
        self.current_time = begin
        # Set Temporary folder
        if not self.full_path:
            self.temp_path = ""
            temp_suffix = ""


            if platform == "win32" and (
                    '{' in temp_suffix or '}' in temp_suffix or ':' in temp_suffix):  # on windows, create a path without special characters
                temp_suffix = temp_suffix.replace(":", "")  # .replace(os.sep,'_')

            self.temp_path = str(os.path.basename(temp_suffix))

            # add most params to path
            hcode = int(sha256(temp_suffix.encode('utf-8')).hexdigest(), 16) % 10 ** 8
            self.temp_path += "_" + str(hcode)
            self.temp_path = join(self.temp_folder, self.temp_path)
        else:
            self.temp_path = self.temp_folder
            self.temp_folder = RemoveLastTokensFromPath(self.temp_folder, 1)[:-1]

            if platform == "win32" and '{:' in self.temp_path:  # on windows, create a path without special characters
                self.temp_path = self.temp_path.replace("{:", "").replace("}", "")

        mkdir(self.temp_folder)
        mkdir(self.temp_path)

        if import_temp:
            if os.path.isfile(temp_archive_path) and temp_archive_path.endswith("zip"):
                import shutil
                shutil.unpack_archive(temp_archive_path, self.temp_path, "zip")

        self.show_raw_t = -1  # default: raw to show is the first one
        self.dataset = Dataset(self, begin, end, raw_dict=raw_data, seg_dict=segment_data, log=self.log, background=background,
                               xml_file=xml_file, temp_path=self.temp_path,segname=segname)

    def set_mesh_parameters(self,factor=1,z_factor=None,raw_factor=1,z_raw_factor=None,smoothing=True,smooth_passband=0.01,
                            smooth_iterations=25,quadric_clustering=True,qc_divisions=1,decimation=True,
                            decimate_reduction=0.8,auto_decimate_threshold=30):
        self.factor = factor
        self.raw_factor=raw_factor
        self.z_raw_factor=z_raw_factor if z_raw_factor is not None else raw_factor
        self.z_factor = z_factor if z_factor is not None else factor
        self.smoothing=smoothing
        self.smooth_passband = smooth_passband
        self.smooth_iterations = smooth_iterations
        self.quadric_clustering = quadric_clustering
        self.qc_divisions = qc_divisions
        self.decimation = decimation
        self.decimate_reduction = decimate_reduction
        self.auto_decimate_threshold = auto_decimate_threshold


    ######################################### PLUGINS

    def add_plugin(self, plugin):
        """ Add a python plugin to be import in the MorphoNet Window

        Parameters
        ----------
        plugin : MorphoPlugin
            A plugin instance

        Examples
        --------
        from plugins.MARS import MARS
        mc.add_plugin(MARS())
        """
        if plugin not in self.plugins:
            self.plugins.append(plugin)
            self._create_plugin(plugin)

    def _create_plugin(self, plug):
        """ Create the plugin in the MorphoNet Window

        Parameters
        ----------
        plug : MorphoPlugin
            A plugin instance

        """
        printv("Create Plugin " + plug.name,2)
        self.send("BTN", plug._get_btn())

        if plug.explanation is not None:
            bdata = plug.explanation_bytes #plug.explanation[:,:,0].tobytes(order="F")
            cmd = "EX_" +str(plug.explanation.shape[0])+"_"+str(plug.explanation.shape[1])+"_"+str(len(plug.explanation_bytes))+"_"+plug.name+"_"+plug.description
            self.send(cmd, bdata)

        if plug.icon is not None:
            bdata = plug.icon_bytes
            cmd = "IC_" +str(plug.icon.shape[0])+"_"+str(plug.icon.shape[1])+"_"+str(len(plug.icon_bytes))+"_"+plug.name
            self.send(cmd, bdata)

    def set_default_plugins(self):
        """ Load the default plugins to the 3D viewer

        Examples
        --------
        mc.set_default_plugins()
        """
        printv("Load plugins...",1)
        from morphonet.plugins import defaultPlugins
        for plug in defaultPlugins:  self.add_plugin(plug)

    def clear_plugins(self):
        """ Clear all preloaded (default ) plugins

        Examples
        --------
        mc.clear_plugins()
        """
        if self.plugins is None or len(self.plugins)==0: return True
        printv("Clear +" +str(len(self.plugins)),2)
        self.plugins.clear()


    ######################################### RAWIMAGES

    def get_temp_raw_filename_at(self,t):
        return get_temp_raw_filename_at(self.dataset.temp_raw_path,t,self.raw_factor,self.z_raw_factor)

    def active_raw(self):
        self.show_raw=True #We said that the menu is open
        self.send("CONTAINSRAW_" + str(self.dataset.begin) + ";" + str(next(iter(self.dataset.nb_raw_channels.values()))))  # Active Button Show Raw in Unity

    def compute_raw(self,t):
        rawdata = None
        raw_filename = self.get_temp_raw_filename_at(t)
        original_rawshape = None
        min_max = None
        try:
            if not isfile(raw_filename):
                printv("ERROR miss temporary file " + raw_filename, -1)
            else:
                data = np.load(raw_filename)
                rawdata = data['raw']
                original_rawshape = data['shape']

                if "voxel_size" in data:
                    self.dataset.set_voxel_size(t, data['voxel_size'])
                if "min_max" in data:
                    min_max = data["min_max"]
        except:
            printv("ERROR reading temporary file " + raw_filename, -1)
        return rawdata,original_rawshape,min_max

    def plot_raw(self, t):
        """ Compute and send raw images to the browser for a specified time point

        Parameters
        ----------
        t : int
            time point to display raw images from

        Examples
        --------
        mc.plot_raw(1)
        """
        if self.dataset.raw: #If there is any raw
            if self.conversion_raw and self.conversion_meshes:  # The Raw Conversion And The Meshes Conversion is done is done
                if self.show_raw_t!=t : #We already send the images
                    if not self.show_raw:   self.active_raw()  # The first time we open the menu

                    printv("Send rawdatas at " + str(t) + " ("+str(self.dataset.nb_raw_channels[t])+" channels) ",1)
                    rawdata,original_rawshape, min_max = self.compute_raw(t)
                    raw_real_size = [-1, -1, -1]

                    #if we cannot get original raw values: we need to compute them and overwrite the npz file
                    if min_max is None:
                        printv(f"Please wait for recomputing of min and max values of intensity images at time {t}", 1)
                        min_max = self.recompute_image_minmax(t,rawdata,original_rawshape)

                    if (self.dataset.raw_dict is not None and str(t) in self.dataset.raw_dict
                            and "0" in self.dataset.raw_dict[str(t)] and "Size" in self.dataset.raw_dict[str(t)]["0"]):
                        raw_real_size = self.dataset.raw_dict[str(t)]["0"]["Size"]

                    if rawdata is not None:
                        bdata = rawdata.tobytes(order="F")
                        cmd = ("RAW_" + str(t) + "_" + str(self.dataset.nb_raw_channels[t])+
                               "_" + str(original_rawshape[0]) + "_" + str(original_rawshape[1]) +
                               "_" + str(original_rawshape[2]) + "_" + str(self.raw_factor) + "_" +
                               str(self.z_raw_factor) + "_" + self.dataset.get_center(txt=True) +
                               "_"+self.dataset.get_voxel_size(t,txt=True) + "_" + str(raw_real_size[0]) +
                               "_" + str(raw_real_size[1]) + "_" + str(raw_real_size[2]) + "_" +
                               str(min_max.tolist()))
                        self.send(cmd, bdata)
                        self.show_raw_t = t

    def recompute_image_minmax(self, t, rawdata, original_rawshape):
        min_max = []
        for c in range(self.dataset.nb_raw_channels[t]):
            raw = self.dataset.get_raw(t,c)
            mi, ma = image_minmax(raw)
            min_max.append(mi)
            min_max.append(ma)
        if rawdata is not None:
            raw_filename = self.get_temp_raw_filename_at(t)
            voxel_size = self.dataset.get_voxel_size(t)
            if voxel_size is not None:
                np.savez_compressed(raw_filename, raw=rawdata, shape=original_rawshape, voxel_size=voxel_size,
                                    min_max=min_max)  # Save in npz
            else:
                np.savez_compressed(raw_filename, raw=rawdata, shape=original_rawshape, min_max=min_max)
        else:
            printv(f"ERROR: Cannot recompute min/max values for raw image(s) at time {t}. "
                   f"original image is missing!", -1)
        return np.asarray(min_max)


    ######################################### ADDD SEEDS

    def plot_seeds(self, seeds):
        """ Plot seeds to the browser

        Parameters
        ----------
        seeds : string
            the centers of the seeds

        Examples
        --------
        mc.plot_seeds(seeds)
        """
        if seeds is not None and seeds != "":
            self.send("SEEDS", seeds)

    ######################################### PRIMITIVES

    def add_primitive(self, name, obj):
        """ Add a primitive using specified content with the specified name to the browser

        Parameters
        ----------
        name : string
            the name of the primitive
        obj : bytes
            content of the primitive (3D data)

        Examples
        --------
        Specify a file on the hard drive by path, with rights
        f = open(filepath,"r+")
        load content of file inside variable
        content = f.read()
        mc.add_primitive("primitive name",content)
        f.close()
        """
        self.send("PRIM_" + str(name), obj)

    ######################################### PROPERTIES

    def _reset_properties(self):
        """
            Reset the updated of all properties
        """
        if self.dataset.properties is not None:
            for property_name in self.dataset.properties:
                pro = self.get_property(property_name)
                pro.updated = False

    def get_property_field(self, property_name):
        """ Called when Unity asked for the txt field of the propety name

        """
        prop = self.get_property(property_name)
        if prop is None or not prop.asked:  #Not loaded yet loaded
            printv("not yet loaded: "+property_name,2)
            if property_name in self.dataset.xml_properties_type: #Confirm that it's in the avaiable xml file
                printv("loading " + property_name+"...", 1)
                self.dataset.read_txt(property_name)

        if self.get_property(property_name) is not None:
            prop = self.get_property(property_name)
            prop.asked = True

        #self.plot_property(self.get_property(property_name))  #Now We plot the property
        self.restart(None)

    def send_properties_name(self):
        """
        Send only the name of the properties that are existing in the xml but not loaded
        """
        if self.dataset.xml_properties_type is not None:
            for property_name in self.dataset.xml_properties_type:
                if self.get_property(property_name) is None or not self.get_property(property_name).asked: #only send property if it does not yet exist in text
                    if self.dataset.xml_properties_type[property_name] != "time":#do not send lineage in names, it should already be sent
                        self.send("INFONAME_" + property_name,self.dataset.xml_properties_type[property_name])
        self.check_exit()

    def plot_properties(self,re_read=False):

        """ Plot all the Properties of the datasset
        """
        if self.dataset.properties is not None:
            for property_name in self.dataset.properties:
                self.plot_property(self.get_property(property_name),re_read=re_read)

    def plot_property(self, property, re_read=False):  # PLOT property
        """ Send the specified properties with the specified name to browser

        Parameters
        ----------
        property : Property Class
           the property to plot

        Examples
        --------
        my_prop=mc.get_property("Cell Name")
        mc.plot_property(my_prop)
        """
        if property is None:
            return None
        text = None
        if property.updated and property.asked or (re_read and property.asked):
            if re_read:  # in case where we have to read the txt property an update: (get the latest file available)
                step_temp_path = join(self.temp_path, str(self.dataset.step))
                txt_file = f"{property.name}.txt"
                index = self.dataset.step
                while not isfile(join(step_temp_path, txt_file)) and index > 0:  # get the latest version of the prop
                    index -= 1
                    step_temp_path = join(self.temp_path, str(index))
                path_text = join(step_temp_path, txt_file)
                if os.path.exists(path_text):
                    printv(f"reloading property {property.name} at step {index}", 1)
                    f = open(path_text, "r+")
                    # load content of file inside variable
                    content = f.read()
                    f.close()
                    property.clear()
                    property.add_data(content)
                    text = content
            if text is None:
                text = property.get_txt(time_begin=self.dataset.begin, time_end=self.dataset.end,empty=True)
            printv("plot " + property.name,1)
            self.send("INFO_" + property.name, text)


    def plot_stop_loading(self):
        printv("DONE", 0)  # To clear unity messages
        printv("Wait for a command", 1)
        self.send("STOPLOAD")

    def plot_annotations(self):

        """ Plot all the annotation for all the properties of the datasset
        """

        if self.dataset.properties is not None:
            for property_name in self.dataset.properties:
                self.plot_annotation(self.get_property(property_name))

    def plot_annotation(self,property):
        """ Send the specified annotation for the properties with the specified name to browser

        Parameters
        ----------
        property : Property Class
           the property to plot
        """

        if property is None:
            return
        if property.property_type!="time" and property.property_type!="label" and property.property_type!="selection":
            txt = property.get_txt(time_begin=self.dataset.begin, time_end=self.dataset.end, all_values=True)
            if txt is not None:
                printv("plot annotation for " + property.name,1)
                self.send("CUR_" + property.name, txt)
            else:
                printv("no annotation for " + property.name, 1)

    def get_properties(self):
        """ Return all the properties associated to the dataset
        """
        return self.dataset.properties

    def get_property(self, property_name):
        """ Return the property associated to the dataset

        Parameters
        ----------
        property_name : string
           the name of the property

        return property :  Property Class
            return an object of property


        Examples
        --------
        my_prop=mc.get_property("Cell Name")
        """
        if property_name in self.dataset.properties:
            return self.dataset.properties[property_name]
        return None

    def create_property(self, property_name, property_type, data=None):
        """ Create an property associated to the dataset

        Parameters
        ----------
        property_name : string
           the name of the property
        property_type
            the type of the property (float,string, etc.. ) in string
        data (optional) : List<string> or property as in MorphoNet
            property content as a list of all lines

        Examples
        --------
        prop=mc.create_property("Cell Name","string")
        prop.set(el,"a7.8")
        """
        prop = self.dataset.get_property(property_name, property_type=property_type, reload=False)
        if data is not None:  prop.add_data(data)
        return prop

    def delete_property(self, property_name):
        """ delete an property associated to the dataset

        Parameters
        ----------
        property_name : string
           the name of the property

        Examples
        --------
        prop=mc.delete_property("Cell Name")
        prop.set(el,"a7.8")
        """
        if property_name in self.dataset.properties:
            self.dataset.properties.remove(property_name)

    def set_property_type(self, property_name, property_type):
        """ Change or specify the type of an property associated to the dataset
            The property can be created directly in python or load in the XML file

        Parameters
        ----------
        property_name : string
          the name of the property
        property_type
           the type of the property (float,string, etc.. )  in string

        Return True if the changement is affected

        Examples
        --------
        mc.set_property_type("ThisField","label")
        """
        prop = self.get_property(property_name)
        if prop is None:
            return False
        prop.property_type = property_type
        return True

    def reload_properties(self):
        self.plot_properties()
        self.plot_annotations()

    def annotate(self, property_name, k, v, d):
        """ Apply the annotation value of a specific object for the property name

        Parameters
        ----------
        property_name : string
           the name of the property
        k : string
            object to annotate
        v : string
            value of annotate
        d : string
            date of annotate
        """
        printv("annotate property " + property_name,1)
        prop = self.get_property(property_name)
        o = self.dataset.get_object(k)
        prop.set(o, v, date=d)
        prop.export()
        prop.export_annotations()
        self.restart(None)

    def delete_annotation(self, property_name, k, v, date=None):
        """ Delete the annotation value of a specific object for the property name

        Parameters
        ----------
        property_name : string
           the name of the property
        k : string
            object to annotate
        v : string
            value of annotation
        """
        prop = self.get_property(property_name)
        o = self.dataset.get_object(k)
        if not prop.del_annotation(o, v, date=date):
            printv(" Error during the deletion of the annotatotion ",1)
        else:
            prop.export()
            prop.export_annotations()
        self.restart(None)

    def create_property_from_unity(self, property_name, property_type, data=None, file=None):
        """ Create or Update property when receiving data from unity

        Parameters
        ----------
        property_name : string
           the name of the property
        property_type : string
            property type
        data : string
            data to write in property file
        file : string
            file from which to extract data
        """
        pro=None
        if data is None or data == "":
            if file is not None and isfile != "":
                if isfile(file):
                    with open(file,"r") as pf:
                        data = pf.read()

        if property_name in self.dataset.properties : #property already exist , it's an update
            if property_type == "label" or property_type == "selection" :
                pro=self.dataset.properties[property_name]
                pro.clear()
            else: printv("this name already exists ",0)# nothing to do, we cannot create two qualitative properties with the exact same name
        else:
            self.dataset.xml_properties_type[property_name] = property_type
            pro = self.dataset.get_property(property_name, property_type=property_type, reload=False)
        if pro is not None:
            if data is not None:  pro.add_data(data)
            pro.asked = True
            pro.export()  # Save It

        self.restart(None)

    def delete_property_from_unity(self, property_name):
        """ Delete property asked from unity

        Parameters
        ----------
        property_name : string
           the name of the property
        """
        printv("delete property " + property_name,1)
        prop = self.get_property(property_name)
        if prop is not None:
            prop.delete(True)
            self.restart(None)

    def delete_label_from_unity(self, property_name):
        """ Delete property when receiving data from unity

        Parameters
        ----------
        property_name : string
           the name of the property
        """
        self.delete_property(property_name)
        self.restart(None)

    def delete_properties(self):
        '''
        Remove In unity the properties which have been deleted in python
        '''
        to_remove=[]
        if self.dataset.properties is not None:
            for property_name in self.dataset.properties:
                prop=self.get_property(property_name)
                if prop.todelete:
                    printv("delete "+property_name,1)
                    self.send("DELINFO_" + property_name) # TODO THE FUNCTION IS NOT EXISTING IN UNITY
                    to_remove.append(prop)
        for prop in to_remove:
            prop.delete() #Full Detion

    ######################################### SCIKIT PROPERTIES

    def plot_regionprops(self):
        """
        Plot all the propeties required by the user
        And send the name that are existing in the xml but not yet asked by the user
        """
        if self.dataset.regionprops is not None:
            for property in self.dataset.regionprops:
                if self.dataset.regionprops[property].asked:  # Update the values if asked
                    self.plot_regionprop(property)

    def plot_regionprop(self, property):  # PLOT Scikiimage property
        """ Send the specified property with the specified name to browser

        Parameters
        ----------
        property : property name
        """
        if self.dataset.regionprops is not None:
            if property in self.dataset.regionprops:
                if not self.dataset.regionprops[property].sent: #We do not resent what is already sent ..
                    printv("Send scikit property " + property, 2)
                    prop_text = self.dataset.regionprops[property].get_txt()
                    self.send("INFO_" + property.replace("_", "-"), prop_text)
                    self.dataset.regionprops[property].sent = True

    def ask_regionprop(self,property):
        """ Called when Unity asked for the property  of the scikit regions property
        """
        printv("Ask scikit property " + property , 2)
        if self.dataset.regionprops is not None:
            if property not in self.dataset.regionprops:  # It's an additional  property asked
                printv("ERROR this " + property+ " does not exist ...",-1)
            else:
                if not self.dataset.regionprops[property].asked : #First time we asked this propery
                    self.dataset.ask_regionprop(property)

        self.restart(None)

    '''def is_all_computed_regionprop(self,name):
        if name not in self.dataset.regionprops:
            return False

        if len(self.dataset.regionprops[name].data)==0:  #Raw only
            return False
        for t in range(self.dataset.begin, self.dataset.end + 1):
            if t in self.dataset.regionprops[name].computed_times:
                for channel in self.dataset.segmented_channels:
                    if channel in self.dataset.regionprops[name].computed_times[t]:
                        if not self.dataset.regionprops[name].computed_times[t][channel]:
                            return False
            else:
                return False

        printv("all time step regions are computed for  "+name,2)
        return True

    def get_regionprops(self, name):
        """ Called when Unity asked for the property  of the scikit regions property
        """
        if self.dataset.regionprops is not None:
            if name not in self.dataset.regionprops: #It's an additional  property asked
                self.dataset.create_regionsprop(name)
                self.dataset.start_load_regionprops() #We relaunch the regions computing system

            printv("Set scikit property "+name+ " loaded",2)
            self.dataset.regionprops[name].asked=True
        self.restart(None)
>>>>>>> main

    def plot_regionprops(self):
        """
        Plot all the propeties required by the user
        And send the name that are existing in the xml but not yet asked by the user
        """
        if self.dataset.regionprops is not None:
            for property in self.dataset.regionprops:
                if self.dataset.regionprops[property].asked:  # Update the values if asked
                    self.plot_regionprop(property)

    def plot_regionprop(self, property):  # PLOT Scikiimage property
        """ Send the specified property with the specified name to browser

        Parameters
        ----------
        property : property name
        """
        if self.dataset.regionprops is not None:
            if property in self.dataset.regionprops:
                if not self.dataset.regionprops[property].sent: #We do not resent what is already sent ..
                    printv("Send scikit property " + property, 2)
                    prop_text = self.dataset.regionprops[property].get_txt()
                    self.send("INFO_" + property.replace("_", "-"), prop_text)
                    self.dataset.regionprops[property].sent = True

    def ask_regionprop(self,property):
        """ Called when Unity asked for the property  of the scikit regions property
        """
        printv("Ask scikit property " + property , 2)
        if self.dataset.regionprops is not None:
            if property not in self.dataset.regionprops:  # It's an additional  property asked
                printv("ERROR this " + property+ " does not exist ...",-1)
            else:
                if not self.dataset.regionprops[property].asked : #First time we asked this propery
                    self.dataset.ask_regionprop(property)

        self.restart(None)

    def delete_region_props(self,t,channel):
        filename = self.dataset.get_last_version(self.dataset.temp_segname.format(int(t), int(channel)))
        if filename is not None and isfile(filename):
            propsfile = self.dataset._regionprops_filename(filename)
            if isfile(propsfile):
                rm(propsfile)
            self.dataset.delete_regionprops_at(t, channel)

    def read_regionprops_from_file(self, file_list, channel):
        import pickle
        if file_list is None: return None
        regionprops = {}
        for time in file_list:
            filename = file_list[time]
            if isfile(filename):
                printv("read properties file " + filename, 1)
                with open(filename, "rb") as infile:
                    prop = pickle.load(infile)
                    for c in prop:
                        for p in prop[c]:
                            if p not in regionprops:
                                regionprops[p] = ScikitProperty(self.dataset, p)
                                regionprops[p].computed_times[time] = {}
                                regionprops[p].computed_times[time][channel] = False
                            regionprops[p].set(self.dataset.get_object(time, c, channel),  prop[c][p])  # FILL THE PROPERTY
        return regionprops

    def plot_regionprop_from_list(self, prop_list):  # PLOT Scikiimage property
        """ Send the specified property with the specified name to browser

        Parameters
        ----------
        name : property name
        """
        if prop_list is not None:
            for name in prop_list:
                printv("Plot scikit property " + name, 2)
                prop_text = prop_list[name].get_txt()
                self.send("INFO_" + name.replace("_", "-"), prop_text)

    def delete_region_props(self,t,channel):
        filename = self.dataset.get_last_version(self.dataset.temp_segname.format(int(t), int(channel)))
        if filename is not None and isfile(filename):
            propsfile = self.dataset._regionprops_filename(filename)
            if isfile(propsfile):
                rm(propsfile)
            self.dataset.delete_regionprops_at(t, channel)

    def read_regionprops_from_file(self, file_list, channel):
        import pickle
        if file_list is None: return None
        regionprops = {}
        for time in file_list:
            filename = file_list[time]
            if isfile(filename):
                printv("read properties file " + filename, 1)
                with open(filename, "rb") as infile:
                    prop = pickle.load(infile)
                    for c in prop:
                        for p in prop[c]:
                            if p not in regionprops:
                                regionprops[p] = ScikitProperty(self.dataset, p)
                                regionprops[p].computed_times[time] = {}
                                regionprops[p].computed_times[time][channel] = False
                            regionprops[p].set(self.dataset.get_object(time, c, channel),  prop[c][p])  # FILL THE PROPERTY
        return regionprops

    def plot_regionprop_from_list(self, prop_list):  # PLOT Scikiimage property
        """ Send the specified property with the specified name to browser

        Parameters
        ----------
        name : property name
        """
        if prop_list is not None:
            for name in prop_list:
                printv("Plot scikit property " + name, 2)
                prop_text = prop_list[name].get_txt()
                self.send("INFO_" + name.replace("_", "-"), prop_text)

    '''
    def send_available_regionprops(self):
        """
        Send the list of avaiable scikit property not computed by default
        """
        printv("Send list of avaiable scikit properties " , 2)
        for name in self.dataset.regionprops:
            prop=self.dataset.regionprops[name]
            self.send("SKINFONAME_" + name.replace('_',"-"), prop.type)

    #########################################  LABEL

    def plot_label(self, label):
        '''
        Plot label (list of objects separated by ;)
        '''
        if label is not None:
            #printv("label " + label,1)
            self.send("SELECT", str(label))

    #########################################  MESH

    def compute_meshes(self,times=None):
        """ Precompute meshes (without any windows visuaslaition)

        Parameters
        ----------
        times : list of int
            List of times steps to compute, None is equal to all

        Examples
        --------
        mc=morphonet.Plot(start_browser=False)
        mc.compute_meshes()
        """
        if times is None:
            times = range(self.dataset.begin, self.dataset.end + 1)
        for t in times:
            for channel in self.dataset.segmented_channels:
                obj = self.compute_mesh(t,channel)
                if obj is None:
                    data = self.dataset.get_seg(t,channel=channel)
                    if data is not None:
                        obj = self.compute_mesh(t, channel,data)
                    self.dataset.seg_datas.clear()

    def compute_obj_path(self,t,channel):
        #We look for the last npz (wich is the required file)
        obj_step=self.dataset.get_last_version(self.dataset.temp_segname.format(int(t), int(channel)),step_only=True)
        filename=str(t)+"_ch"+str(channel)+".obj"
        obj_path = join(self.temp_path, str(obj_step))
        if obj_step != self.dataset.step:  # The folder is different of the current one
            if self.dataset.cells_updated is not None and t in self.dataset.cells_updated and channel in self.dataset.cells_updated[t]:
                if self.dataset.cells_updated[t][channel] is None or len(self.dataset.cells_updated[t][channel]) > 0: #CELLS TO UPDATED
                    obj_path = self.dataset.step_folder
        obj_filename = join(obj_path, filename)
        return obj_filename,obj_path

    def compute_mesh(self, t,channel, data=None, filename=None, force_recompute=False):

        '''

        Compute Mesh for a given channel at a given time point

        '''

        if t not in self.dataset.cells_updated: self.dataset.cells_updated[t] = {}  #The first start , we use the precomputed cell
        if channel not in self.dataset.cells_updated[t]: self.dataset.cells_updated[t][channel]=[]
        if filename is None:
            filename,obj_path= self.compute_obj_path(t,channel)
        else:
            obj_path=os.path.dirname(filename)
        if not isfile(filename): #No need to try to compute if file is empty
            if data is None: return None
        printv("Compute mesh at " + str(t) + " to "+filename, 2)
        bbox = None
        if not force_recompute:
            bbox=self.dataset.get_regionprop_at("bbox",t,channel) # need regionproperties for mesh generation

        obj = fast_convert_to_OBJ(data, bbox=bbox, t=t, background=self.dataset.background, channel=channel,factor=self.factor,
                                  center=self.dataset.get_center(),VoxelSize=self.dataset.get_voxel_size(t),
                                  cells_updated=self.dataset.cells_updated[t][channel],path_write=obj_path,
                                  write_vtk=True,force_recompute=self.recompute,
                                  z_factor=self.z_factor,Smooth=self.smoothing,smooth_passband=self.smooth_passband,
                                  smooth_iterations=self.smooth_iterations,Decimate=self.quadric_clustering,
                                  QC_divisions=self.qc_divisions,
                                  Reduction=self.decimation,TargetReduction=self.decimate_reduction,
                                  DecimationThreshold=self.auto_decimate_threshold)  # Create the OBJ


        if obj is None and data is not None:
            printv("Unable to compute mesh at time : "+str(t)+" please verify your path to segmentation", 0)
        if data is not None:
            self.dataset.cells_updated[t][channel] = [] #We don' want to reset if nothing was recalculated
        return obj

    def get_mesh_object(self,mo):
        """
        Return the mesh (in obj) for a given cell
        (Read the vtk temporart file and convert it to obj)
        """
        obj_step = self.dataset.get_last_version(str(mo.t) +"_ch"+str(mo.channel)+".obj", step_only=True) #Look for the location of th last time point
        obj_mesh_path = join(self.temp_path, str(obj_step),str(mo.t)+","+str(mo.channel))
        if not isdir(obj_mesh_path):
            printv("error did not find the temporary mesh path "+obj_mesh_path, 1)
            return None
        cell_mesh_filename=join(obj_mesh_path,str(mo.t)+'-'+str(mo.id)+'.vtk')

        if not isfile(cell_mesh_filename):
            printv("error did not find the temporary cell mesh file " + cell_mesh_filename, 1)
            return None

        #Convert VTK in OBJ
        obj=convert_vtk_file_in_obj(cell_mesh_filename, mo, ch=mo.channel, factor=self.factor, center=self.dataset.get_center(), VoxelSize=self.dataset.get_voxel_size(mo.t))
        return obj

    def delete_mesh_at(self,t,channel,filename=None):
        if filename is None : filename, obj_path = self.compute_obj_path(t, channel)
        if filename is not None and isfile(filename):
            rm(filename)
        #DELETE VTK
        vtk_path=join(os.path.dirname(filename),str(t)+","+str(channel))
        if isdir(vtk_path):   rmrf(vtk_path)
        else:printv("Warning vtk path does not exist "+vtk_path,2)

    def recompute_raw(self):
        #DELETE RAW
        #init_raw from dataset
        if self.dataset.temp_raw_path is None or self.dataset.temp_raw_path == "":
            self.temp_raw_path = join(self.temp_path, "raw")
        rmrf(self.dataset.temp_raw_path)
        mkdir(self.dataset.temp_raw_path)
        self.dataset.init_raw()

    def delete_seg_at(self, t, channel, delete_file=True, filename=None):
        if delete_file:
            if filename is None:
                filename = self.dataset.get_last_version(self.dataset.temp_segname.format(int(t), int(channel)))
            if os.path.isfile(filename):
                rm(filename)
        if t in self.dataset.seg_datas:
            if channel in self.dataset.seg_datas[t]:
                del self.dataset.seg_datas[t][channel]


    def recompute_data(self,region_props=False,seg=False,meshes=False,raw=False):
        """ Force computation of meshes and properties for all time points
        """
        self.recompute=True
        printv("Recompute data ", 1)
        times = range(self.dataset.begin, self.dataset.end + 1)
        self.dataset.init_channels()
        #reset center:
        center_file = join(self.temp_path, "center.npy")
        if isfile(center_file):  rm(center_file)

        if seg: #We have to recompute all (images are differents)
            region_props=True
            meshes=True
        if region_props:  meshes=True

        last_step=self.dataset.get_last_step()
        for temp_step in range(last_step+1):
            for t in times:
                for channel in self.dataset.segmented_channels:
                    filename = join(self.temp_path, str(temp_step), self.dataset.temp_segname.format(int(t), int(channel)))
                    if isfile(filename): #ONLY IF THIS TIME STEP WAS MODIFIED
                        delete_file=False
                        if seg and temp_step==0: # Changement possible before curation only ! So we do not have the look in all steps
                            printv(f"Delete seg  at {t} channel ={channel}", 2)
                            delete_file=True

                        self.delete_seg_at(t, channel,delete_file=delete_file)
                        data = self.dataset.get_seg(t, channel=channel,  filename=filename)  # We have to update the data at this step
                        if region_props:
                            region_filename=self.dataset._regionprops_filename(filename)
                            printv(f"Delete region prop {region_filename}", 2)
                            self.dataset.delete_regionprops_at(t,channel,filename=region_filename,delete_file=True)
                            self.dataset.compute_regionprops_at(t, channel, recompute=True, filename=region_filename)

                        if meshes:
                            filename = join(self.temp_path, str(temp_step), str(t) + "_ch" + str(channel) + ".obj")
                            printv(f"Delete mesh {filename}", 2)
                            self.delete_mesh_at(t,channel,filename=filename)
                            obj = self.compute_mesh(t, channel, data=data, filename=filename)

        if raw:
            self.recompute_raw()
        self.recompute=False

    def plot_steps_number(self):
        """
        Plot the current steps status (visualisation and current step)

        Examples
        --------
        mc.plot_steps_number()
        """
        printv(f"Curation step number {self.dataset.visualization_step} (of {self.dataset.step})", 1)
        self.send("STEP_" + str(self.dataset.visualization_step) + ";" + str(self.dataset.step))

    def plot_meshes(self, times=None, channels=None):  # PLOT ALL THE TIMES STEP EMBRYO IN MORPHONET
        """ Plot all data inside the browser

        Examples
        --------
        mc.plot_meshes()
        """
        printv("Plot Meshes...", 1)
        if times is None:
            times = range(self.dataset.begin, self.dataset.end + 1)
        if channels is None:
            channels = self.dataset.segmented_channels
        for t in times:
            for channel in channels:
                self.plot_mesh(t, channel)

        self.conversion_meshes = True
        self.check_exit()

    def plot_mesh(self, t,channel):  # UPLOAD DIRECTLY THE OBJ TIME POINT IN UNITY
        """ Send the 3D files for the specified time point to browser and display the mesh

        Parameters
        ----------
        t : int
            the time point to display in browser
        channel :
                None -> all segmentation channels
                int -> sepcific segmentation channel
        Examples
        --------
        mc.plot_mesh(1)
        """
        printv("Load mesh at " + str(t)+ " for channel "+str(channel), 0)
        obj = self.compute_mesh(t,channel) #We first look if a temporary file is available (ONLY WHEN NO cells_updated)
        if obj is None:
            data = self.dataset.get_seg(t,channel=channel)
            if data is not None:
                obj = self.compute_mesh(t, channel ,data)
        if obj is not None:
            self.plot_obj_at(t,channel,obj)
        self.check_exit()

    def plot_obj_at(self, t, channel, obj):  # PLOT DIRECTLY THE OBJ PASS IN ARGUMENT
        """ Plot the specified 3D data to the specified time point inside the browser

        Parameters
        ----------
        t : int
            the time point to display in browser
        obj : bytes
            the 3d data

        Examples
        --------
        #Specify a file on the hard drive by path, with rights
        f = open(filepath,"r+")
        #load content of file inside variable
        content = f.read()
        mc.plot_at(1,content)
        f.close()
        """
        self.send("LOAD_" + str(t) + ";" + str(channel), obj)

    def plot_step(self, step_number):
        """ This function plot directly the obj and the properties of a specific step to the visualization , without storing it in python memory

        Parameters
        ----------
        step_number : int
        """
        printv("Plot step for visualization : "+str(step_number)+ " (current "+str(self.dataset.visualization_step)+")", 1)
        #We first list the files change between the current step
        if step_number < self.dataset.visualization_step:  # BACKWARD
            step_to_cancel = self.dataset.visualization_step  # Get previous visualisation Step
        else:
            step_to_cancel=step_number
        step_temp_path = join(self.temp_path, str(step_to_cancel))  # path to the step folder to cancel if we have to
        if not isdir(step_temp_path):
            printv("miss step to cancel " + str(step_to_cancel), -1)
            return False
        next_step_path = join(self.temp_path, str(step_number))
        # This section is called if you try to plot a step where the obj / region file is missing for a specific npz file
        if os.path.isdir(next_step_path):
            printv("Verifying files consistency ",1)
            for f in os.listdir(next_step_path):
                if f.endswith(".npz"):
                    time_point, channel = get_tc_from_filename(f, ".npz")
                    prop_file = join(next_step_path,f.replace(".npz",".regions.pickle"))
                    if not isfile(prop_file):
                        printv("Properties file missing for time point  "+str(time_point)+ " and channel "+str(channel) +" -> Recomputing", 0)
                        self.dataset.compute_voxel_regionprops_at(time_point, channel, filename=prop_file)
                        self.dataset.compute_voxel_regionprops_at(time_point, channel, voxel=False, filename=prop_file)
                    obj_file = join(next_step_path,str(time_point) +"_ch"+str(channel)+".obj")
                    if not isfile(obj_file):
                        printv("Mesh file missing for time point  " + str(time_point) + " and channel " + str(
                            channel) + " -> Recomputing", 0)
                        data, vs = _load_seg(join(next_step_path,f))
                        obj = self.compute_mesh(time_point, channel, data=data, filename=join(next_step_path,f),force_recompute=True)

        file_to_reload = []
        if os.path.isdir(step_temp_path):
            for f in os.listdir(step_temp_path):
                if f.endswith(".obj") or f.endswith("regions.pickle"):  # List all obj to load
                    file_to_reload.append(f)
        if len(file_to_reload) == 0:
            printv("nothing to reload ", 2)

        for f in file_to_reload:
            last_file=None
            if f.endswith(".obj") or  f.endswith("regions.pickle"):
                if step_number < self.dataset.visualization_step:  # BACKWARD
                    last_file = self.dataset.get_last_version(f, before=step_to_cancel)
                else:  # FORWARD
                    last_file = join(step_temp_path, f)
            if last_file is not None:

                if f.endswith(".obj"):  # List all obj to load
                    t, channel = get_tc_from_filename(f, ".obj")
                    self.plot_obj_at(t, channel, read_mesh(last_file))
                if f.endswith("regions.pickle"):  # Read region prop
                    t, channel = get_tc_from_filename(f, ".regions.pickle")

                    self.dataset.delete_regionprops_at(t,channel)
                    self.dataset.read_regionprops_at(t, channel,  filename = last_file)

                    self.dataset.update_cells_at(t,channel)

        self.dataset.visualization_step = step_number
        self.plot_regionprops()

        #PROPERTY: reload properties to their last version in history
        prev_property_files = [f for f in os.listdir(step_temp_path) if f.endswith(".txt")]
        # path to start looking for to find last properties versions
        index = step_number
        step_prop_path = join(self.temp_path, str(index))
        # for all properties
        for txt_file in prev_property_files: # for each previous prop: get the oldest version (we have to update)
            filename = txt_file.split(".")[0]
            propname = filename.replace(".txt", "")
            if propname in self.dataset.properties:  # if prop is in dict
                if self.dataset.properties[propname].asked:
                    while not isfile(join(step_prop_path,txt_file)) and index > 0: # get the latest version of the prop
                        index -= 1
                        step_prop_path = join(self.temp_path, str(index))
                    path_text = join(step_prop_path,txt_file)
                    if not isfile(path_text):
                        printv(f"Warning: could not find last version of property {propname}. did not exist in previous steps",1)
                    else:
                        f = open(path_text, "r+")
                        # load content of file inside variable
                        content = f.read()
                        f.close()
                        self.send("INFO_" + filename, content)


        self.plot_steps_number()


    def del_mesh(self, t):  # DELETE DITECLTY THE OBJ TIME POINT IN UNITY
        """ Delete the specified time point in the browser

        Parameters
        ----------
        t : int
            the time point to delete

        Examples
        --------
        mc.del_mesh(1)
        """
        self.send("DEL_" + str(t))

    ################ TO QUIT PROPERLY
    def clear_backup(self):
        '''
        To Clear backup files
        '''
        rmrf(self.temp_path)

    def _receive_signal(self, signalNumber):
        if signalNumber == 2:
            self.quit_and_exit()
        return
