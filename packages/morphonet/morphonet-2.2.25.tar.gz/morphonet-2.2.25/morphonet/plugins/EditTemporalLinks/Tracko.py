# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from morphonet.tools import printv
import numpy as np

######## OVERLAP BY BBOX
def get_iou_bbox(bb1, bb2):
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

def get_best_overlap_bbox(bbox,bboxs):
    o=0
    best=None
    #computing the best = one by one computing
    for mo in bboxs:
        #get the iou count for the box
        ov=get_iou_bbox(bbox,bboxs[mo])
        #if iou is more than the previous best, choose this box
        if ov>o:
            o=ov
            best=mo
    return best,o


######## OVERLAP BY MASK

def IOU_cell(cell_gt, cell_pd):  # GT AND PD AS TO BE BINARY (TRUE / FALSE OR 0,1)
    val = np.uint8(cell_gt) + np.uint8(cell_pd)
    vals, vals_nb = np.unique(val, return_counts=True)
    vals1 = vals_nb[vals == 1][0] if 1 in vals else 0
    vals2 = vals_nb[vals == 2][0] if 2 in vals else 0
    iou = 0 if vals1 == 0 and vals2 == 0 else np.float32(vals2) / np.float32(vals1 + vals2)
    return iou


def bbox_overlap(bbox1, bbox2):
    bbox = np.zeros([6, ])
    for i in range(3):
        bbox[i] = min(bbox1[i], bbox2[i])
    for i in range(3):
        bbox[i + 3] = max(bbox1[i + 3], bbox2[i + 3])
    return np.uint16(bbox)


def get_best_overlap_iou(mo,image1,bbox1,image2,next_bbox,bboxs):
    databox1 = image1[bbox1[0]:bbox1[3], bbox1[1]:bbox1[4], bbox1[2]:bbox1[5]]
    cell1_mask = databox1 == mo.id

    databox2 = image2[next_bbox[0]:next_bbox[3], next_bbox[1]:next_bbox[4], next_bbox[2]:next_bbox[5]] #Next Bounding Box (might be deform by optical flow)
    ids = np.unique(databox2[cell1_mask])
    ids=ids[ids!=0] #Remove Background
    o = 0
    best = None
    for cell2 in ids:
        bbox2=None
        for mo2 in bboxs:
            if mo2.id==cell2:
                bbox2 = bboxs[mo2]
        bbox12 = bbox_overlap(bbox1, bbox2)
        databox1 = image1[bbox12[0]:bbox12[3], bbox12[1]:bbox12[4], bbox12[2]:bbox12[5]]
        databox2 = image2[bbox12[0]:bbox12[3], bbox12[1]:bbox12[4], bbox12[2]:bbox12[5]]
        iouc = IOU_cell(databox1 == mo.id, databox2 == cell2)
        if iouc > o:
            o = iouc
            best = cell2
    if best is not None: #Find back the objects
        printv(f"best iou ({mo.id} ; {best}) : {o}",2)
        for mo2 in bboxs:
            if mo2.id==best:
                return mo2, o
        printv(f" Error did not find the object {best} in bbox : {bboxs}",2)
    return best, o

def get_best_match(box_ids):
    ids, counts = np.unique(box_ids, return_counts=True)
    id_best = np.argsort(-counts)[0]
    cell2 = ids[id_best]
    if cell2 == 0:  # Background get the next one
        ids = list(ids)
        del ids[id_best]
        counts = list(counts)
        del counts[id_best]
        if len(counts) == 0: return 0  # Only match with background
        id_best = np.argsort(-np.array(counts))[0]
        cell2 = ids[id_best]
    return cell2

def get_best_overlap_mask(mo,image1,bbox1,image2,next_bbox,bboxs):
    databox1 = image1[bbox1[0]:bbox1[3], bbox1[1]:bbox1[4], bbox1[2]:bbox1[5]]
    cell1_mask = databox1 == mo.id

    databox2 = image2[next_bbox[0]:next_bbox[3], next_bbox[1]:next_bbox[4], next_bbox[2]:next_bbox[5]] #Next Bounding Box (might be deform by optical flow)
    cell2 = get_best_match(databox2[cell1_mask])

    if cell2>0: #Not in the bacgrund  is not None: #Find back the objects
        for mo2 in bboxs:
            if mo2.id==cell2:
                return mo2, 1
    return None, None



def get_overlap_iou(mo,image1,bbox1,image2,next_bbox,bboxs):
    databox1 = image1[bbox1[0]:bbox1[3], bbox1[1]:bbox1[4], bbox1[2]:bbox1[5]]
    cell1_mask = databox1 == mo.id

    databox2 = image2[next_bbox[0]:next_bbox[3], next_bbox[1]:next_bbox[4], next_bbox[2]:next_bbox[5]] #Next Bounding Box (might be deform by optical flow)
    ids = np.unique(databox2[cell1_mask])
    ids = ids[ids != 0]  # Remove Background
    ious={}
    for cell2 in ids:
        bbox2=None
        for mo2 in bboxs:
            if mo2.id==cell2:
                bbox2 = bboxs[mo2]
        bbox12 = bbox_overlap(bbox1, bbox2)
        databox1 = image1[bbox12[0]:bbox12[3], bbox12[1]:bbox12[4], bbox12[2]:bbox12[5]]
        databox2 = image2[bbox12[0]:bbox12[3], bbox12[1]:bbox12[4], bbox12[2]:bbox12[5]]
        ious[cell2] = IOU_cell(databox1 == mo.id, databox2 == cell2)
    return ious

def get_overlap_bbox(bbox,bboxs):
    ious = {}
    for mo in bboxs:
        iou=get_iou_bbox(bbox,bboxs[mo])
        if iou>0:ious[mo]=iou
    return ious

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


def remove_link_with(links,matches,one_link):
    new_links={}
    nb_c2={} #Count usage in current Matches
    for c1 in matches:
        c2=matches[c1]
        if c2 not in nb_c2:nb_c2[c2]=1
        else:nb_c2[c2]+=1
    for c1 in links:
        if c1 not in matches: #Remove the first one, it already matched
            new_ious = {}
            ious=links[c1]
            for c2 in ious:
                if c2 not in nb_c2 or (nb_c2[c2]<2 and not one_link) or  (nb_c2[c2]<1 and one_link):
                    new_ious[c2]=ious[c2]
            if len(new_ious)>0:
                new_links[c1]=new_ious
    return new_links

class Tracko(MorphoPlugin):
    """This plugin creates a complete object lineage using the maximum of overlap between objects.
    The overlap is calculated between the bounding box enveloping each object. After the execution, the lineage property
    is updated. This plugin requires a segmentation.


    Parameters
    ----------
    intensity_channel: int, default: 0
        The desired channel of the intensity images used for tracking
    downsampling : int, default: 2
        Downsampling applied to intensity images, the higher the downsampling , the faster the plugin will run, but worse the result quality
    time_direction : list
        Forward : The  tracking is performed from the current time point to last one.
        Backward : The tracking is performed from the current time point to first one
    optical_flow : string
        none : No optical flow.
        TV-L1 : TV-L 1 optical flow method https://scikit-image.org/docs/0.23.x/api/skimage.registration.html#skimage.registration.optical_flow_tvl1
        iLK :iterative Lucas-Kanade pptical flow  method   https://scikit-image.org/docs/0.23.x/api/skimage.registration.html#skimage.registration.optical_flow_ilk
    number of links:
        all : create all possible links (backward and forward mode)
        2: can create 2 daughters links, in backward mode only  (in forward, it creates only 1 link)
        1: create only 1 links (backward and forward mode)

    """
    def __init__(self): #PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_image_name("Tracko.png")
        self.set_icon_name("Tracko.png")
        self.set_name("Track : Create temporal links on all objects using maks overlap between time steps")
        self.set_parent("Edit Temporal Links")
        self.add_inputfield("Intensity channel", default=0)
        self.add_dropdown("time direction", ["forward", "backward"])
        self.add_dropdown("optical flow", ["none","TV-L1", "iLK"])
        self.add_dropdown("number of links", ["2", "1","all"])
        self.add_inputfield("downsampling", default=2)
        self.add_toggle("on labeled", default=False)

    def make_links(self, bboxs, next_bboxs, ious, matches, flow, downsampling, init_shape, number_of_links,
                   direction, clear_links = False):


        links = {}  # Only used to keep all possibilites for recursive mode
        for mo in bboxs:
            bb = bboxs[mo]
            flow_bb = bb
            if flow is not None:
                bb = np.uint16(np.array(bb) / downsampling)
                vectors = flow[bb[0]:bb[3], bb[1]:bb[4], bb[2]:bb[5], :]
                vector = [vectors[..., 0].mean(), vectors[..., 1].mean(),
                          vectors[..., 2].mean()]  # Average the displacement
                vector = vector * 2  # Duplicate the list

                flow_bb = np.uint16(bb + vector)
                if downsampling > 1:  flow_bb *= downsampling
                flow_bb[flow_bb < 0] = 0  # Restore outliers
                flow_bb[3] = min(flow_bb[3], init_shape[0])
                flow_bb[4] = min(flow_bb[4], init_shape[1])
                flow_bb[5] = min(flow_bb[5], init_shape[2])

            if number_of_links == "all":
                next_mo, o = get_best_overlap_bbox(flow_bb,
                                                   next_bboxs)  # For each box at t , find the best overlapping one at t+1
            else:  # 2 or 1 link
                links[mo] = get_overlap_bbox(bb, next_bboxs)
            '''elif overlap == "mask":
                next_mo,o = get_best_overlap_mask(mo, seg_t, bb, seg_tp, flow_bb,next_bboxs) #NOT USED  YET TODO : Test and Debug
            elif overlap=="iou":
                next_mo, o = get_best_overlap_iou(mo, seg_t, bb, seg_tp, flow_bb, next_bboxs) #NOT USED, YET  quite slow TODO : Test and Debug
            '''

            if number_of_links == "all":
                ious[mo] = o
                matches[mo] = next_mo

        if number_of_links != "all":  # Now we match the best first
            while len(links) > 0:
                c1, c2, o = get_best_links(links)
                ious[c1] = o
                matches[c1] = c2
                links = remove_link_with(links, matches, number_of_links == "1")

        for mo, v in sorted(ious.items(), key=lambda item: item[1], reverse=True):
            next_mo = matches[mo]
            printv(f"Match {mo.id} with {next_mo.id} with iou={v}", 2)

            if clear_links: #  if we want to clear the previous links before setting them:
                if direction == "backward":
                    ms = mo.mothers.copy()
                    for mot in ms:
                        self.dataset.del_mother(mo, mot)
                    # Remove daughter links in lineage
                if direction == "forward":
                    ds = mo.daughters.copy()
                    for daugh in ds:
                        self.dataset.del_daughter(mo, daugh)

            self.dataset.add_daughter(mo, next_mo) if direction == "forward" else self.dataset.add_daughter(next_mo,
                                                                                                            mo)  # link the corresponding cells in lineage

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects,objects_require=False):
            return None
        #Get the lineage propagation direction
        direction=self.get_dropdown("time direction")
        optical=self.get_dropdown("optical flow")
        number_of_links = self.get_dropdown("number of links")
        downsampling = int(self.get_inputfield("downsampling"))
        channel = int(self.get_inputfield("Intensity channel"))
        on_labeled = bool(self.get_toggle("on labeled"))

        printv(f"start overlap tracking from {t}",0)
        if direction=="forward" :
            while t<self.dataset.end: #From t to t max
                # compute lineage by overlaping
                self.compute_links(t,t+1,channel,optical,downsampling,direction,number_of_links,objects,on_labeled)
                t+=1
        if direction == "backward":
            while t > self.dataset.begin: #from t to t min
                # compute lineage by overlaping
                self.compute_links(t, t - 1,channel,optical,downsampling,direction,number_of_links,objects,on_labeled)
                t -= 1

        self.restart()

    def compute_links(self,t, tp, channel,optical,downsampling, direction,number_of_links,objects=None, on_labeled=False):
        from skimage.registration import optical_flow_ilk, optical_flow_tvl1

        printv(f"compute links at {t}, channel {channel}", 0)
        flow = None
        init_shape = None
        if optical != "none":
            rawdata0 = self.dataset.get_raw(t, channel)
            rawdata1 = self.dataset.get_raw(tp, channel)
            if rawdata0 is None or rawdata1 is None:
                printv("cannot use optical flow without intensity images", 0)
            else:
                m = max(rawdata0.max(), rawdata1.max())
                init_shape = rawdata0.shape
                if downsampling > 1:
                    rawdata0 = rawdata0[::downsampling, ::downsampling, ::downsampling]
                    rawdata1 = rawdata1[::downsampling, ::downsampling, ::downsampling]

                #Pass in 8 bit
                rawdata0 = np.uint8(rawdata0 * 255.0 / m)
                rawdata1 = np.uint8(rawdata1 * 255.0 / m)
                printv(f"Compute optical flow {optical} at {t}", 1)
                if optical != "iLK":
                    flow = optical_flow_ilk(rawdata0, rawdata1)
                else:
                    flow=optical_flow_tvl1(rawdata0, rawdata1)

                flow = np.swapaxes(flow, 0, 3)
                flow = np.swapaxes(flow, 0, 2)
                flow = np.swapaxes(flow, 0, 1)


        bboxs = self.dataset.get_regionprop_at("bbox", t, channel) #Get the different cells bounding box
        next_bboxs = self.dataset.get_regionprop_at("bbox", tp, channel) #Get the next time points bounding box
        #In case of only one link , we first have to calculate the iou for all cells and then order them to attribue only one line
        ious={}
        matches={}

        if on_labeled and objects is not None:  #  if the option is activated: work on the selections
            bbox = None  # Get the bounding box around the selected cells
            to_link = {}
            next_to_link = {}
            for o in self.dataset.get_objects_at(objects, t):
                if o.s not in to_link:
                    to_link[o.s] = []
                to_link[o.s].append(o)

            for o in self.dataset.get_objects_at(objects, tp):
                if o.s not in next_to_link:
                    next_to_link[o.s] = []
                next_to_link[o.s].append(o)

            for selection in to_link: #  compute per selection
                if selection in next_to_link:
                    bbs = {k: v for k, v in bboxs.items() if k in to_link[selection]}
                    next_bbs = {k: v for k, v in next_bboxs.items() if k in next_to_link[selection]}
                    s_ious = {}
                    s_matches = {}
                    self.make_links(bbs, next_bbs, s_ious, s_matches, flow, downsampling, init_shape, number_of_links,
                                    direction, clear_links=True)

        else:
            self.make_links(bboxs,next_bboxs,ious,matches,flow,downsampling,init_shape,number_of_links,direction)
