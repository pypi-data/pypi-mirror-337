# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from ..functions import  get_borders
from ...tools import printv


class Seedis(MorphoPlugin):
    """ This plugin generates seeds that can be used in other plugins (mainly watershed segmentation).
    \n
    This plugin requires at least one selected object.
    The plugin computes the distance to the border of the selected objects and then extracts the maxima.
    N seeds are generated at the maximal distance inside the selected object (N being the number of seeds to generate),
    if the distance (between seeds) is above the threshold given by the min_distance parameter (in voxels, not
    physical size).



    Parameters
    ----------
    nb_seeds : int, default: 2
        the number of seeds to generate in each object (> 1)
    min_distance : int, default: 30
       The minimum allowed distance (number of voxels) separating peaks. To find the maximum number of peaks,
       use min_distance=1.

    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_parent("De Novo Seeds")
        self.set_icon_name("Seedis.png")
        self.set_image_name("Seedis.png")
        self.set_name("Seedis : Create seeds from the maximum distance to the border of the selected objects (without intensity images)")
        self.add_inputfield("nb seeds", default=2)
        self.add_inputfield("min distance", default=30)

    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects, backup=False):
            return None

        from scipy import ndimage as ndi
        from skimage.feature import peak_local_max
        import numpy as np
        Nb_Seeds = int(self.get_inputfield("nb seeds"))
        min_distance = int(self.get_inputfield("min distance"))

        nbc = 0
        for channel in dataset.get_channels(objects):  # For each channels in selected object
            for t in dataset.get_times(objects):  # For each time point in cells labeled
                data = dataset.get_seg(t,channel)#Load segmentation data in memory
                #For each cell to this time point
                for o in dataset.get_objects_at(objects, t):
                    #Get the coordinates in the image
                    cellCoords=dataset.np_where(o)
                    printv('Look for object ' + str(o.get_name()) + " with " + str( len(cellCoords[0])) + " voxels ",0)
                    #Get the bounding box of the ojects
                    xmin, xmax, ymin, ymax, zmin, zmax = get_borders(data, cellCoords)
                    cellShape = [1 + xmax - xmin, 1 + ymax - ymin, 1 + zmax - zmin]
                    mask = np.zeros(cellShape, dtype=bool)
                    mask[cellCoords[0] - xmin, cellCoords[1] - ymin, cellCoords[2] - zmin] = True
                    #Get the array of distances to the background for each voxel
                    distance = ndi.distance_transform_edt(mask)
                    #Get the local maximas of this distances
                    peak_idx = peak_local_max(distance, min_distance=min_distance, num_peaks=Nb_Seeds)
                    #Add a seed to each maxima
                    for i in range(len(peak_idx)):
                        cc=peak_idx[i]
                        coord = [cc[0] + xmin, cc[1] + ymin, cc[2] + zmin]
                        dataset.add_seed(coord)
                        nbc += 1
        #Restart to morphonet
        printv("Found " + str(nbc) + " new seeds",0)
        self.restart()

