# -*- coding: latin-1 -*-
from os.path import join, isfile, basename, abspath,dirname
from skimage.transform import resize
from morphonet.plugins import MorphoPlugin
import numpy as np
from ...tools import printv, cp, rmrf
from ..functions import get_torch_device, read_time_points, donwsample


def denoise_train(denoise_model,rawdata,data,t):
    from skimage.measure import regionprops
    #Denoise rawdata with CellPose3 but not working yet.
    if denoise_model is not None:
        printv("denoise z planes  at " + str(t), 0)
        for z in range(rawdata.shape[2]):
            regions=regionprops(data[...,z])
            diameter=0.0
            nbdiameter=0
            for r in regions:
                if r['label']!=0:
                    diameter+=r['equivalent_diameter_area']
                    nbdiameter+=1
            if nbdiameter>0:   diameter/=nbdiameter
            else : diameter=30 #Default value
            printv("denoise z planes  " + str(z) + "  at " + str(t)+ " with average diameter "+str(diameter), 1)
            rawdata[..., z] = denoise_model.eval(rawdata[..., z], channels=[0, 0], diameter=diameter)[..., 0]
    return rawdata

def make_isotrope(rawdata,data,voxel_size):
        anisotropy = voxel_size[2] / voxel_size[1]  # 1/0.2=5 -> 100,100,20 ->  100,100,20*5
        if anisotropy != 1:
            printv(f"found anisotropy of {anisotropy}", 1)
            rawdata = resize(rawdata, [rawdata.shape[0], rawdata.shape[1], int(anisotropy * rawdata.shape[2])],
                             preserve_range=True).astype(rawdata.dtype)
            data = resize(data, [data.shape[0], data.shape[1], int(anisotropy * data.shape[2])], preserve_range=True,
                          order=0).astype(data.dtype)
        return rawdata,data



class CellposeTrain(MorphoPlugin):
    """
    This plugin allows users to train their own model (from the models provided by CellPose) on their own 3D
    datasets. With an intensity image and the corresponding segmentation, you can re-train a cellpose model to obtain
    your own model, trained on your images. The model will be trained by using 2D images, which are the image stacks on
    the XY, XZ and YZ planes of your 3D images.

    You can use this plugin:

    * on the whole image by not selecting any object.

    * on a sub-part of the image by selecting objects. The algorithm will then run on the masks of ALL the segmented \
    objects found in the bounding box containing all the selected objects.

    The model you output from this plugin can then be used in the Cellpose prediction plugin, by inputting it in the
    pretrained_model parameter.

    Parameters
    ----------
    intensity_channel: int, default : 0
        in case of multiples channel, this corresponds to the intensity images channel

    epochs : int, default : 20
        number of epochs of training

    dimension : string
        For 2D: use XY planes to train.
        For 3D: extract XY, YZ,YX planes to train

    time_points: string
        on which time point to train (current, begin:end, time1;time2;...)

    number_2D_images_per_epochs: int, default : 8
        batch size

    downsampling : int, default :2
        The resolution reduction applied to each axis of the input image before performing segmentation, 1 meaning that
        no reduction is applied. Increasing the reduction factor may reduce segmentation quality

    model_type : string
        The model used to compute segmentations. A detailed documentation on models can be found https://cellpose.readthedocs.io/en/latest/models.html

    model_filename: string
        full filename path to save the model

    isotrope: bool, default: True
        resize (or not) the image to be isotropic before training

    Reference
    ---------
        Stringer, C., Wang, T., Michaelos, M. et al. Cellpose: a generalist algorithm for cellular segmentation.
        Nat Methods 18, 100?106 (2021). https://doi.org/10.1038/s41592-020-01018-x
        https://www.cellpose.org
    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("CellposeTrain.png")
        self.set_image_name("CellposeTrain.png")
        self.set_name("CellPose Train  : Train the CellPose model on your own data")
        self.add_inputfield("Intensity Channel", default=0)
        self.add_inputfield("downsampling", default=1)
        self.add_inputfield("epochs", default=20)
        self.add_dropdown("model type",['cyto','cyto2','cyto3','nuclei','tissuenet','livecell', 'general','CP', 'CPx', 'TN1', 'TN2', 'TN3', 'LC1', 'LC2', 'LC3', 'LC4'])
        self.add_toggle("Isotrope", default=True)
        self.add_inputfield("time points", default="current")
        self.add_inputfield("number 2D images per epochs", default=8)
        #self.add_dropdown("denoise model type",['no-denoising', 'denoise-cyto3', 'deblur-cyto3', 'upsample-cyto3', 'denoise-nuclei','deblur-nuclei', 'upsample-nuclei'])
        self.add_filesaver("model filename")
        self.set_parent("De Novo Segmentation")

    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects, objects_require=False):
            return None

        from cellpose import models
        import logging
        logging.basicConfig(level=logging.INFO) #To have cellpose log feedback on the terminalk

        which,device=get_torch_device(mps=False) #Seems that we cannot train when MPS architecture is active ...
        printv("CellPose Train will run on " + which, 1)

        intensity_channel= int(self.get_inputfield("Intensity Channel"))
        downsampling = int(self.get_inputfield("downsampling"))
        model_type = self.get_dropdown("model type")
        n_epochs = int(self.get_inputfield("epochs"))
        nimg_per_epoch=int(self.get_inputfield("number 2D images per epochs"))
        Isotrope = self.get_toggle("Isotrope")

        #We first same the model in a temporary Path
        model_filename=self.get_filesaver("model filename")
        train_dir = dataset.parent.temp_path
        printv(f" temporary train path is {train_dir}",2)
        model_name=basename(model_filename)

        denoise_model = None
        '''
        #FOR CELLPOSE 3 but not working yet ...
        denoise_model_type = self.get_dropdown("denoise model type")
        if denoise_model_type != "no-denoising":
            from cellpose.denoise import DenoiseModel
            denoise_model = DenoiseModel(model_type=denoise_model_type.replace("-", "_"), gpu=True)
        '''
        learning_rate = 0.1
        weight_decay = 0.0001
        channels = [0,0]

        train_data = []
        train_labels = []
        nb_cells = 0

        if len(objects)>=1 and objects[0]!="":
            for t in dataset.get_times(objects):  # Get all times in the labeled objects list
                rawdata = dataset.get_raw(t, intensity_channel)
                data = dataset.get_seg(t, intensity_channel)
                if rawdata is not None and data is not None:

                    if Isotrope:  rawdata,data=make_isotrope(rawdata,data,dataset.get_voxel_size(t))
                    if downsampling > 1: rawdata,data=donwsample(rawdata,data,downsampling)
                    if dataset.background != 0: data[  data == dataset.background] = 0  # We do it after the rescaling to go faster
                    if denoise_model is not None: rawdata = denoise_train(denoise_model, rawdata, data, t)

                    bbox = None  # Get the bounding box arround the selected cells
                    for o in dataset.get_objects_at(objects, t):
                        printv("add object " + str(o.id) + " at " + str(o.t), 1)
                        bb = dataset.get_regionprop("bbox", o)
                        if bbox is None:
                            bbox = bb
                        else:
                            bbox = [min(bb[0], bbox[0]), min(bb[1], bbox[1]), min(bb[2], bbox[2]), max(bb[3], bbox[3]),
                                    max(bb[4], bbox[4]), max(bb[5], bbox[5])]

                    rawdata_box = rawdata[bbox[0]:bbox[3] + 1, bbox[1]:bbox[4] + 1, bbox[2]:bbox[5] + 1]
                    data_box=data[bbox[0]:bbox[3] + 1, bbox[1]:bbox[4] + 1, bbox[2]:bbox[5] + 1]

                    for dim in range(3):
                        for c in range(data_box.shape[dim]):  # ADD Slicdes
                            if dim == 0:
                                rawslice = rawdata_box[c, ...]
                                segslice = data_box[c, ...]
                            elif dim == 1:
                                rawslice = rawdata_box[:, c, :]
                                segslice = data_box[:, c, :]
                            else:
                                rawslice = rawdata_box[..., c]
                                segslice = data_box[..., c]

                            im = np.reshape(rawslice, (1,) + rawslice.shape)
                            cells = np.unique(segslice)
                            if len(cells) > 5:  # Minimum Pixels Required by Cell Pose
                                train_data.append(im)
                                train_labels.append(segslice)
                                nb_cells += len(cells) - 1

        else: #TRAIN ON THE FULL IMAGE
            times=read_time_points(self.get_inputfield("time points"),t)
            if len(times)==0:
                printv("No time points",0)
            else:
                printv(f" Train on {times} time point",2)

                for t in times: # Colllect the selected data at the given time point
                    rawdata = dataset.get_raw(t, intensity_channel)
                    data = dataset.get_seg(t, intensity_channel)

                    if Isotrope:  rawdata, data = make_isotrope(rawdata, data, dataset.get_voxel_size(t))
                    if downsampling > 1: rawdata, data = donwsample(rawdata, data, downsampling)
                    if dataset.background != 0: data[ data == dataset.background] = 0  # We do it after the rescaling to go faster
                    if denoise_model is not None: rawdata = denoise_train(denoise_model, rawdata, data, t)


                    for dim in range(3):
                        for c in range(data.shape[dim]): #ADD Slicdes
                            if dim==0:
                                rawslice=rawdata[c,...]
                                segslice=data[c,...]
                            elif dim==1:
                                rawslice = rawdata[:,c,:]
                                segslice = data[:,c,:]
                            else:
                                rawslice = rawdata[...,c]
                                segslice = data[...,c]

                            im = np.reshape(rawslice, (1,) + rawslice.shape)
                            cells = np.unique(segslice)
                            if len(cells) > 5:  # Minimum Pixels Required by Cell Pose
                                train_data.append(im)
                                train_labels.append(segslice)
                                nb_cells += len(cells) - 1

        if len(train_data)==0 or nb_cells==0:
            printv("ERROR Cannot Train with not images or no cells",0)
        else:
            printv(f"{nb_cells} objects added at {t}", 0)
            printv(f"Start Train CellPose on {len(train_data)} 2D images from model : {model_type}",0)

            if isfile(model_filename): #Continue to train
                printv(f"Found a pretrained model, continue to train on {model_filename}",1)
                model = models.CellposeModel(gpu=which=="GPU", device=device, pretrained_model=model_filename)
            else:
                model = models.CellposeModel(gpu=which=="GPU", device=device, model_type=model_type)

            #CELLPOSE 3
            #from cellpose import train
            #model_path = train.train_seg(model.net, train_data=train_data, train_labels=train_labels,  channels=channels,   save_path=train_dir,   n_epochs=n_epochs,   normalize=True,    learning_rate=learning_rate,   weight_decay=weight_decay,   nimg_per_epoch=nimg_per_epoch,  model_name=model_name)

            #CELLPOSE 2
            model_path = model.train(train_data, train_labels,
                                     channels=channels,
                                     save_path=train_dir,
                                     n_epochs=n_epochs,
                                     normalize=True,
                                     learning_rate=learning_rate,
                                     weight_decay=weight_decay,
                                     nimg_per_epoch=nimg_per_epoch,
                                     model_name=model_name)


            if not isfile(join(train_dir,"models",model_name)): #CellPose automaticaly add "models"
                printv("Error miss temporary model  "+str(join(train_dir,"models",model_name)),0)
            else:
                cp(join(train_dir,"models",model_name),dirname(abspath(model_filename)))
                if not isfile(model_filename):
                    printv(f"Training error, miss  model  {model_filename}", 0)
                    printv("look in the temporary folder "+str(join(train_dir,"models",model_name)),1)
                else:
                    printv(f"Model Saved into {model_filename}",0)
                    rmrf(join(train_dir,"models"))  #Delete temporary folder

        logging.basicConfig(level=logging.WARNING)
        self.restart(cancel=True) #We do not change anything
