# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from morphonet.tools import printv
import numpy as np

def get_iou(bb1, bb2):
    '''
    Calculate the Intersection over Union (IoU) of two bounding boxes.
    '''

    # determine the coordinates of the intersection rectangle
    x_left = max(bb1[0], bb2[0])
    y_top = max(bb1[1], bb2[1])
    z_up = max(bb1[2], bb2[2])
    x_right = min(bb1[3], bb2[3])
    y_bottom = min(bb1[4], bb2[4])
    z_down = min(bb1[5], bb2[5])

    if x_right < x_left or y_bottom < y_top  or z_down< z_up :
        return 0.0

    # The intersection of two axis-aligned bounding boxes is always an
    # axis-aligned bounding box
    intersection_area = (x_right - x_left) * (y_bottom - y_top) * (z_down - z_up)

    # compute the area of both AABBs
    bb1_area = (bb1[3] - bb1[0]) * (bb1[4] - bb1[1]) * (bb1[5] - bb1[2])
    bb2_area = (bb2[3] - bb2[0]) * (bb2[4] - bb2[1]) * (bb2[5] - bb2[2])

    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
    return iou



def get_best_overlap(bbox,bboxs):
    o=0
    best=None
    #computing the best = one by one computing
    for mo in bboxs:
        #get the iou count for the box
        ov=get_iou(bbox,bboxs[mo])
        #if iou is more than the previous best, choose this box
        if ov>o:
            o=ov
            best=mo
    return best,o

def bbox_overlap(bbox1, bbox2):
    bbox = np.zeros([6, ])
    for i in range(3):
        bbox[i] = min(bbox1[i], bbox2[i])
    for i in range(3):
        bbox[i + 3] = max(bbox1[i + 3], bbox2[i + 3])
    return np.uint16(bbox)

def get_bbox(bboxs,c_id):
    for mo in bboxs:
        if mo.id==c_id:
            return bboxs[mo]
    return None
def IOU_cell(cell_gt, cell_pd):  # GT AND PD AS TO BE BINARY (TRUE / FALSE OR 0,1)
    val = np.uint8(cell_gt) + np.uint8(cell_pd)
    vals, vals_nb = np.unique(val, return_counts=True)
    vals1 = vals_nb[vals == 1][0] if 1 in vals else 0
    vals2 = vals_nb[vals == 2][0] if 2 in vals else 0
    iou = 0 if vals1 == 0 and vals2 == 0 else np.float32(vals2) / np.float32(vals1 + vals2)
    return iou

def generate_combinations(lst):
    from itertools import combinations
    all_combinations = []
    for r in range(1, len(lst) + 1):
        all_combinations.extend(combinations(lst, r))
    return all_combinations

def get_best_links(links):
    best=0
    best_match=None
    for c1 in links:
        ious=links[c1]
        for c2 in ious:
            if ious[c2]>best:
                best=ious[c2]
                best_match=(c1,c2,best)
    printv(f"best match : {best_match} ",2)
    return best_match

def remove_link(links,matches,remove_c1=None):
    new_links={}
    associated=[]
    for c1 in matches: associated.append(matches[c1])
    for c1 in links:
        if c1 not in matches and c1!=remove_c1: #Remove the first one, it already matched
            new_ious = {}
            ious=links[c1]
            for c2 in ious:
                if c2 not in associated:
                    new_ious[c2]=ious[c2]
            if len(new_ious)>0:
                new_links[c1]=new_ious
    return new_links

class TrackAndFuse(MorphoPlugin):
    """Starting from a good segmentation at the given time point, this plugin propages this segmentation to the next time points using the maximum overlap between the objects.
    When multiples objects overlap to the same one (potential cell division), the plugin fuse the objects together if the ratio with the previous one is under the value Morther/Daughter ratio
    This plugin works only in forward mode from the current time point.
    The overlap is calculated between the bounding box enveloping each object.
    After the execution, the lineage property is updated.
    The plugin erase previous lineage before creating new temporal links
    This plugin requires a segmentation.


    Parameters
    ----------
    Segmentation channel : int
        channel on which to apply the plugin
    Mother daughter ratio : float
        Threshold ratio of mother/daughter volume to determine if we fuse a cell
    Number of time steps : int
        Number of time steps to track and fuse. e.q. on time 7, to track and fuse to time 10 enter a value of 3

    """
    def __init__(self): #PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_image_name("TrackAndFuse.png")
        self.set_icon_name("TrackAndFuse.png")
        self.set_name("TrackFuse : Fuse small cells and generate lineage")
        self.set_parent("Propagate Segmentation")
        self.add_inputfield("Segmentation channel", default=0)
        self.add_inputfield("mother daughter ratio", default=3)
        self.add_inputfield("number of time steps", default=1)

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects,objects_require=False):
            return None
        #Get the lineage propagation direction
        channel = int(self.get_inputfield("Segmentation channel"))
        timestep = int(self.get_inputfield("number of time steps"))
        daughters_ratio = float(self.get_inputfield("mother daughter ratio"))

        last_time_step = t + timestep
        if last_time_step > self.dataset.end:
            last_time_step = self.dataset.end
        printv("start overlap tracking from "+str(t),0)
        while t < last_time_step: #From t to t max
            printv("compute links at " + str(t)+", channel "+str(channel), 0)
            tp=t+1

            bboxs_t = self.dataset.get_regionprop_at("bbox", t, channel)  # Get the different cells bounding box
            seg_t = self.dataset.get_seg(t, channel)
            seg_tp =  self.dataset.get_seg(tp, channel)

            #First we look at all assigned element in the linegage
            volumes = self.dataset.get_regionprop_at("volume", t, channel)
            next_volumes = self.dataset.get_regionprop_at("volume", tp, channel)
            cells_updated=[]
            links = {}
            inv_links = {}
            for c1 in bboxs_t:
                #all cells in this box
                bbox=bboxs_t[c1]

                databox_t = seg_t[bbox[0]:bbox[3], bbox[1]:bbox[4], bbox[2]:bbox[5]]
                cell_mask = databox_t == c1.id
                databox_tp = seg_tp[bbox[0]:bbox[3], bbox[1]:bbox[4], bbox[2]:bbox[5]]
                counts={}
                ids,count = np.unique(databox_tp[cell_mask],return_counts=True)
                for i in range(len(ids)):
                    if ids[i]>0:
                        c2=self.dataset.get_object_at(tp,ids[i])
                        counts[c2]=count[i]
                        if c2 not in inv_links:inv_links[c2]={}
                        inv_links[c2][c1]=count[i]
                links[c1]=counts

            #We first match all the maximum overlap
            ious={}
            matches = {}
            inv_matches=[]
            while len(links) > 0:
                c1, c2, o = get_best_links(links)
                if c2 not in inv_matches: #Not already assigned (Forbidenn 2 mothers -> 1 Daughter-
                    ious[c1] = {}
                    ious[c1][c2]=o
                    matches[c1] = [c2]
                    inv_matches.append(c2)
                    links = remove_link(links, matches)
                else:
                    if c1 in links: del links[c1]


            #Now we look for the non attrivue element
            for c2 in inv_links:
                if c2 not in inv_matches:
                    printv(f"try to find a match for {c2.id} at {c2.t}",2)

                    best=0
                    best_cell=None
                    for c1 in inv_links[c2]:
                        v= inv_links[c2][c1]
                        if v>best:
                            best=v
                            best_cell=c1
                    if best_cell is None or best_cell not in matches:
                        printv(f"did not find any matches for {c2.id}",2)
                    else:
                        ratio=volumes[best_cell]/next_volumes[c2]
                        printv(f"Found a match between  {c2.id} v={next_volumes[c2]}and {best_cell.id} v={volumes[best_cell]} with ratio {ratio}",2)
                        if ratio>daughters_ratio:
                            c2_match=matches[best_cell][0]
                            printv(f"fuse cell {c2.id} with {best_cell.id} at {best_cell.t} which is associated with {c2_match.id} at {c2_match.t}",1)
                            # remove links before you fuse a cell
                            ds = c2.daughters.copy()
                            for daugh in ds:
                                self.dataset.del_daughter(c2, daugh)
                            ms = c2.mothers.copy()
                            for moth in ds:
                                self.dataset.del_mother(c2, moth)
                            dataset.set_cell_value(c2, c2_match.id) #Fuse with he maximum
                            if c2.id not in cells_updated: cells_updated.append(c2.id)
                            if c2_match.id not in cells_updated:  cells_updated.append(c2_match.id)
                        else: #Create a daughter
                            printv(
                                f"link {best_cell.id} at {best_cell.t}  to daughter {c2.id}  at {c2.t}",
                                1)
                            if c2 not in inv_matches: #This cell is not already match with some else (Forbiden 2 mothers -> 1 Daughter)
                                matches[best_cell].append(c2)
                                ious[best_cell][c2]=best
                            else:
                                printv(
                                    f"cell {c2.id}  at {c2.t} is already match",
                                    1)

            for c1 in matches:
                #remove links before you create them
                ds = c1.daughters.copy()
                for daugh in ds:
                    self.dataset.del_daughter(c1, daugh)
                #then you can create the new matches
                for c2 in matches[c1]:
                    printv(f"match {c1.id} with {c2.id} with overlap {ious[c1][c2]}", 1)
                    self.dataset.add_daughter(c1, c2)

            t=tp

            # Change the segmentation
            if len(cells_updated) > 0:
                dataset.set_seg(tp, seg_tp, channel=channel, cells_updated=cells_updated)
            # Send data to morphonet
        self.restart()
