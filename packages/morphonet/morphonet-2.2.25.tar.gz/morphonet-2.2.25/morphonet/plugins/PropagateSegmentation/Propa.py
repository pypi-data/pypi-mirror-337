# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from ...tools import printv


def get_overlap_bbox(bboxs):
    bboxs=[list(bbox) for bbox in bboxs]
    init_bbox=bboxs[0]
    for bbox in bboxs:
        if bbox[0] < init_bbox[0]: init_bbox[0]=bbox[0]
        if bbox[1] < init_bbox[1]: init_bbox[1] = bbox[1]
        if bbox[2] < init_bbox[2]: init_bbox[2] = bbox[2]
        if bbox[3] > init_bbox[3]: init_bbox[3] =bbox[3]
        if bbox[4] > init_bbox[4]: init_bbox[4] = bbox[4]
        if bbox[5] > init_bbox[5]: init_bbox[5] = bbox[5]
    return init_bbox


class Propa(MorphoPlugin):
    """This plugin propagates labeled objects at the current time point through time.\n

    It requires a segmentation, and labeled objects across several time points using labels. Optionally, it can work
    with intensity images as well.

    It requires applying a specific label to the objects to propagate at the current time (named the source objects)
    And then label the corresponding objects on which to propagate at the next or previous time points (named the
    destination objects). The plugin can be executed Forward (source objects are at the beginning of the time range) or
    Backward (source objects are at the end of the time range). The  source objects are eroded until they fit into
    destination objects at the next time point, and then a watershed is computed. The watershed algorith can be
    computed using an intensity image by checking the "use intensity" box. The new objects created by a watershed will
    replace the destination objects.

    Parameters
    ----------
    objects:
        The selected or labeled objects on MorphoNet
    time_direction : string
        Forward : The first time point to be propagated is the lowest one.
        Backward : THe first time point to be propagated is the latest, and the propagation happens in backwards direction
    use_intensity: bool
        Use intensity images for watershed
    intensity_channel: int
        The selected or labeled objects on MorphoNet
    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("Propa.png")
        self.set_image_name("Propa.png")
        self.set_name("Propa : Propagate selected eroded objects through time on the next object (with or without intensity images)")
        self.add_dropdown("time direction", ["Forward", "Backward"])
        self.add_toggle("use intensity",False)
        self.add_inputfield("intensity channel","0")
        self.add_inputfield("minimum volume", default=100)
        self.set_parent("Propagate Segmentation")


    # For time t , and a list of object that will be used as seeds, do a watershed in objects to split
    def process_at(self, t, channel, next_t, objects,objects_next, dataset,prev_t, raw, raw_channel, min_voxels):
        import numpy as np
        from skimage.segmentation import watershed

        from skimage.transform import rescale, resize

        printv("Processing Shape Propagation of " + str(len(objects)) + " objects from time " + str(t) , 0)
        printv("Found  " + str(len(objects_next)) + " objects at time " + str(next_t), 1)
        data_t = dataset.get_seg(t,channel) # Load current time point segmentation
        data_next_t = dataset.get_seg(next_t,channel)# Load next time point segmentation


        #Compute the overlap Bouding Box for the present and futur objects
        bb=None
        for o in objects+objects_next:
            bbox_c = dataset.get_regionprop("bbox", o)
            if bb is None: bb=bbox_c
            else: bb=get_overlap_bbox([bb,bbox_c])
        printv("The largest bounding box is "+str(bb),3)

        #Calculate Final Mask
        sm = data_next_t[bb[0]:bb[3], bb[1]:bb[4], bb[2]:bb[5]]
        mask_next_t = sm == -1  # To Create a mask with only False value
        for o in objects_next:  mask_next_t[sm == o.id] = True  # Binarize

        #Get only the corresponding  mask in the bouding box
        printv("Create markers by overlaping at " + str(t), 1)
        markers = np.zeros_like(mask_next_t).astype(np.uint8)
        smt = data_t[bb[0]:bb[3], bb[1]:bb[4], bb[2]:bb[5]]
        i = 1
        for o in objects:
            sm_id = smt == o.id  # Binarize
            sm_id[mask_next_t==False]=False #Remove the outsides voxel with no overlapping with the next mask
            markers[sm_id] = i
            i += 1

        labels = np.unique(markers)
        if len(labels)<3:
            raise ValueError("Error, masks for cells have no overlap. aborting... ")

        #Now we expand the data in z if necessary
        vsize = dataset.get_voxel_size(t)  # Get the voxelsize
        ratioz = vsize[2] / vsize[0]
        mask_w=1 - np.uint8(mask_next_t)
        if ratioz>1:
            mask_w = resize(mask_w,[mask_w.shape[0],mask_w.shape[1],int(mask_w.shape[2]*ratioz)],preserve_range=True,order=0)
            markers = resize(markers, [markers.shape[0], markers.shape[1], int(markers.shape[2] * ratioz)], preserve_range=True, order=0)

        printv("Compute watershed at "+str(next_t), 1)
        if raw:
            raw = dataset.get_raw(t,channel)
            s_raw = raw[bb[0]:bb[3], bb[1]:bb[4], bb[2]:bb[5]]
            if ratioz>1:
                s_raw = resize(s_raw, [mask_w.shape[0], mask_w.shape[1], int(mask_w.shape[2] * ratioz)], preserve_range=True)
            labelw = watershed(s_raw, markers, mask=1 - mask_w)
        else:
            labelw = watershed(mask_w, markers, mask=1-mask_w)

        if ratioz > 1:
            labelw = resize(labelw, mask_next_t.shape, preserve_range=True, order=0)

        labels, counts = np.unique(labelw, return_counts=True)

        bigest_id=labels[counts==counts[1:].max()][0]
        labels=labels[labels!=0] #Remove background

        printv("Found " + str(len(labels)) + " objects ", 1)

        labels = labels[labels != bigest_id] #Remove the Bigest ID which will be the rest of the mask !!

        cells_updated=[o.id for o in objects_next]
        lastID = int(data_next_t.max()) + 1

        for l in labels:
            new_coords = np.where(labelw == l)
            if len(new_coords[0]) > min_voxels:
                data_next_t[new_coords[0] + bb[0], new_coords[1] + bb[1], new_coords[2] + bb[2]] = lastID
                printv('Create a new object ' + str(lastID) + " with " + str(len(new_coords[0])) + " voxels",1)
                cells_updated.append(lastID)
                lastID+=1
            else:
                printv(f"Cannot create new object, as it would only contain {len(new_coords[0])} voxels", 1)

        next_cells = []
        if len(cells_updated) > 0: # only continue if we have created at least one object.

            # set the new segmentation
            printv(f"the cells {cells_updated} where updated at {t}", 1)
            dataset.set_seg(next_t, data_next_t, channel, cells_updated=cells_updated)

            #Remove the previous links betwen theses elements
            for o in objects:
                for o_next in objects_next:
                    dataset.del_link(o,o_next)

            for o in objects:
                # Future
                bb = dataset.get_regionprop("bbox", o)
                labels, counts = np.unique(data_next_t[bb[0]:bb[3], bb[1]:bb[4], bb[2]:bb[5]], return_counts=True)
                idc = {}
                for i in range(len(labels)):
                    idc[labels[i]] = counts[i]
                idc = {k: v for k, v in idc.items() if k in cells_updated}
                labels = np.asarray(list(idc.keys()))
                counts = np.asarray(list(idc.values()))

                bigest_id = labels[counts == counts.max()][0]
                m = dataset.get_object(next_t, bigest_id, channel)
                dataset.add_link(o, m)



            next_cells=[dataset.get_object(next_t,id, channel) for id in cells_updated]
        return next_cells, data_next_t # Return the list of cells updated, and the new segmentation

    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects):
            return None

        printv("Shape Propagation of " + str(len(objects)) + " objects", 0)
        selections = {} # List Objects by selections , to work on each selection one by one
        for cid in objects:
            o = dataset.get_object(cid)
            if o is not None:
                if o.s not in selections:
                    selections[o.s] = []
                selections[o.s].append(o)

        if len(selections) > 1:
            printv(" --> Found  " + str(len(selections)) + " selections ", 0)

        forward = (str(self.get_dropdown("time direction")) == "Forward")  # Get user direction chosen
        raw = bool(self.get_toggle("use intensity"))
        raw_channel = int(self.get_inputfield("intensity channel"))
        min_volume = int(self.get_inputfield("minimum volume"))

        new_labels = None

        # For each selection found
        for s in selections:
            # Find the min, max and list of times
            time_lists = sorted([o.t for o in selections[s]])
            channel_lists = sorted([o.channel for o in selections[s]])
            channel_lists = list(dict.fromkeys(channel_lists))
            if not forward:time_lists=reversed(time_lists)

            object_times={}

            time_lists = list(dict.fromkeys(time_lists))
            for t in time_lists:
                object_times[t]=[o for o in selections[s] if o.t==t]

            if len(object_times) < 2:
                printv(f"Warning: for time {t}, you need to label at least one cell on the previous/next "
                       f"time step for this plugin to work", 0)

            for channel in channel_lists:
                for t in object_times: # For each time point of this Selection
                    next_t = t + 1 if forward else t - 1 # Detect the time point to modify using direction chosen
                    prev_t = t - 1 if forward else t + 1 # Detect the time point to modify using direction chosen
                    if next_t in object_times: # If the user labeled a cell at the time point to propagate
                        # Propagate the seeds and get the new cells created as source for the next propagation
                        object_times[next_t], data = self.process_at(t, channel, next_t, object_times[t],
                                                                     object_times[next_t],dataset, prev_t, raw,
                                                                     raw_channel,min_volume)

                        # Add the updated cells to the list of cells to update
                        for cell in object_times[next_t]:
                            if new_labels is None:  new_labels = ""
                            new_labels += str(next_t) + "," + str(cell) + "," + str(s) + ";"
        # Send back data to MorphoNet
        self.restart(label=new_labels)
