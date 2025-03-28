# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
import numpy as np
import tqdm

from morphonet.tools import printv, imsave


class Deli(MorphoPlugin):
    """ This plugin remove objects under a certain volume in the segmented image. Please refer to the volume property
    to see the volume value for your segmented image.

    Parameters
    ----------
    minimum_volume: int, default: 20
        The threshold value of the volume (in number of voxels) allowed for the objects to be deleted (>=0)
    time_points: string
        Current times : will only delete all objects at the current time point.
        All times : will delete all objects at all time points
    association : string
        Determines how the deleted objects will be modified:
        Background  : The dataset background value will replace the object label inside the segmented image.
        Closest object : The object to remove will be fused with the object sharing the most contact surface. Objects can be fused with the background.
    segmentation_channel: int, default: 0
        The desired channel to perform the plugin

    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("Deli.png")
        self.set_image_name("Deli.png")
        self.set_parent("Segmentation Correction")
        self.set_name("Deli : Delete any objects below a certain size")
        self.add_inputfield("Segmented channel", default=0)
        self.add_inputfield("minimum volume", default=50)
        self.add_dropdown("time points", ["Current time", "All times"])
        self.add_dropdown("association", ["Closest object", "Background"])

    def remove_under_at(self, t, channel, dataset, associated, volume):
        from scipy.ndimage.morphology import binary_dilation
        data = dataset.get_seg(t,channel)  # Read the data (if not in memory)

        cell_volume = dataset.get_regionprop_at("volume", t, channel, ordered=True)  # Find the volume of the cell , using scikit properties
        cell_updated = []
        nb_objects_delete=0
        cell_to_remove=[]
        cell_to_remove_id = []
        for cell in cell_volume:  # We precompute the list of removing cell to avoid to affect to them
            if cell_volume[cell] < volume:
                cell_to_remove.append(cell)
                cell_to_remove_id.append(cell.id)
        if len(cell_volume) == len(cell_to_remove):
            raise ValueError(f"Error Deli: the volume selected would delete all cells for time {t}, channel {channel}."
                             f" Aborting...")
        for cell in tqdm.tqdm(cell_to_remove):
                id_cell = dataset.background  # if not closes object, will be background
                if associated == "Closest object":  # If user specified closest object
                    # Find the cell borders
                    data_cell = dataset.get_mask_cell(cell, border=5)
                    mask_cell = np.zeros_like(data_cell).astype(np.uint8)
                    mask_cell[data_cell == cell.id] = 1

                    dilate_mask = binary_dilation(mask_cell).astype( np.uint8)  # dilate the cell borders to get the identifiers of voxels around
                    dilate_mask = np.logical_xor(dilate_mask, mask_cell)
                    id_pixels = data_cell[dilate_mask == 1]
                    ids, counts = np.unique(id_pixels, return_counts=True)

                    #Can not affect to cell which will be delete
                    n_ids=[]
                    n_counts=[]
                    for i in range(len(ids)):
                        if ids[i] not in cell_to_remove_id:
                            n_ids.append(ids[i])
                            n_counts.append(ids[i])
                    ids=np.array(n_ids)
                    counts=np.array(n_counts)

                    if len(n_counts)>0:
                        idx = np.where(counts == counts.max())  # Find the one with the most contact
                        id_cell = ids[idx][0]

                if id_cell!=dataset.background:
                    printv("fuse object " + str(cell.id) + " at " + str(cell.t) + ", channel " + str(cell.channel) +
                           " with " + str(int(round(cell_volume[cell]))) + " voxels with " + str(id_cell),
                           2)  # Small cell get this neighbor identifier now (can be background)

                    cell_updated.append(id_cell)  # List of cells that have been updated by the deletion

                else:  # Else , id_cell become background
                    printv("delete object " + str(cell.id) + " at " + str(cell.t) + ", channel " + str(cell.channel) +
                           " with " + str(int(round(cell_volume[cell]))) + " voxels", 2)

                nb_objects_delete+=1
                dataset.set_cell_value(cell, id_cell)  # Update the cell value in image and morphonet

                for m in cell.mothers:  # Destroy the links in the lineage of the old cell
                    dataset.del_mother(cell, m)
                for d in cell.daughters:
                    dataset.del_daughter(cell, d)
                dataset.del_cell_from_properties(cell)
                cell_updated.append(cell.id)  # List of cells that have been updated by the delete

        printv(f"{nb_objects_delete} objects with a volume under {volume} where reassigned at {t} channel {channel}", 0)

        # If the code updated one cell, store the segmentation in morphonet, and recompute everything
        if len(cell_updated) > 0:
            dataset.set_seg(t, data, channel, cells_updated=cell_updated)
            return True
        return False

    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects, objects_require=False):
            return None

        # Get user choice on association , the closest object = the neighbor with most contact, else background
        associated = str(self.get_dropdown("association"))
        segmented_channel = int(self.get_inputfield("Segmented channel"))
        volume = float(self.get_inputfield("minimum volume"))  # Minimum voxel size considered as an object
        cancel=True
        if str(self.get_dropdown("time points")) == "All times":  # should we process at current time or all times
            for i in range(self.dataset.begin, self.dataset.end + 1):
                if self.remove_under_at(i, segmented_channel, dataset, associated, volume):
                    cancel=False
        else:
            if self.remove_under_at(t, segmented_channel, dataset, associated, volume):
                cancel = False

        self.restart(cancel=cancel)  # Send new data and properties to MorphoNet
