import os
import cv2
import time
import detectron2
import torch
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import os, json, cv2, random

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.checkpoint import DetectionCheckpointer
from detectron2.modeling import build_model
from functions import detect_nearest_neighbours, mid_point, change_2_red

classes = ['person', 'mask', 'nomask']

def load_models():
    global classes
    
    cfg = get_cfg()
    model_yaml = "COCO-Detection/faster_rcnn_R_50_FPN_1x.yaml"
    cfg.merge_from_file(model_zoo.get_config_file(model_yaml))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.65  # set threshold for this model
    # cfg.MODEL.WEIGHTS = "output/model_final.pth"
    cfg.MODEL.WEIGHTS = "model_facemask_n_socialdistance.pth"
    # cfg.MODEL.WEIGHTS = "/content/drive/My Drive/datasets/facemask/detectron_d4_faster_rcnn_R_50_FPN_1x/model_final.pth"
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = len(classes)
    cfg.MODEL.DEVICE = "cpu"
    predictor = DefaultPredictor(cfg)
    model = build_model(cfg)
    _ = DetectionCheckpointer(model).load(cfg.MODEL.WEIGHTS)
    return cfg, predictor, model

def print_total_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    frameno = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if frame is None:
            break
        frameno += 1
    print("Total frame:", frameno)
    cap.release()

def process_bulk_frames(frameno, imgs):
    imgs_ = [torch.from_numpy(np.transpose(img, [2, 0, 1])) for img in imgs]
    data = [{'image': img_} for img_ in imgs_]
    with torch.no_grad():
        starttime = time.time()
        outputs = model(data)
        model_time = time.time() - starttime
    print(frameno, "batch_size:", len(imgs), imgs[0].shape, model_time)
    return outputs

def process_single_frame(frameno, img, predictor):
    starttime = time.time()
    outputs = predictor(img)
    model_time = time.time() - starttime

#     if frameno % 10 == 0:
    print(frameno, "batch_size:", 1, img.shape, model_time)
    return outputs

def compute_final_frame(imgs, outputs, frameno, outputfile):
    frameno = frameno - len(imgs) + 1
    for cntr, img in enumerate(imgs):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        '''
        Todo: Generate a Top down view to remove false positives.
        Eg. In case of fixed camera locate the parallel lanes and use this to compute 
        top down view and then run algorithm
        '''
        """ Human Distancing Model """
        # Run the Model on our frame image

        pred_classes = outputs[cntr]['instances'].pred_classes.cpu().numpy()
        bbox = outputs[cntr]['instances'].pred_boxes.tensor.cpu().numpy()

        # Filter for Person instances
        ind = np.where(pred_classes==0)[0]

        # After finding all the persons compute their midpoints, here we can tune the algorithm.
        person = bbox[ind]
        midpoints = [mid_point(img, person,i) for i in range(len(person))]
        num = len(midpoints)

        # dist = compute_distance(midpoints, num)
        #  person_1, person_2, distances = find_closest(dist, num, thresh)
        thresh = 100
        person_1, person_2, distances = detect_nearest_neighbours(midpoints, num, thresh)
        img = change_2_red(img, person, person_1, person_2)
        cv2.putText(img, "Frame: " + str(frameno + cntr), (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

        height, width, layers = img.shape
        size = (width, height)

        """ Face Detection Model """
        scores = outputs[cntr]['instances'].scores.cpu().numpy()
        predictions = outputs[cntr]['instances'].pred_classes.cpu().numpy()
        for i in range(len(scores)):
            if classes[predictions[i]] == "person":
                continue

            box = outputs[cntr]['instances'].pred_boxes[i].__dict__['tensor'].cpu().numpy()[0]
            x1, y1, x2, y2 = box

            _ = cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (255, 255, 255), 1)
            # _ = cv2.circle(img, mid, 3, (0, 255, 0), -1)
            text = "%s %d %%" % (classes[predictions[i]], int(scores[i] * 100))

            color = (255, 0, 0)
            if classes[predictions[i]] == "mask":
                color = (0, 255, 0)
            _ = cv2.rectangle(img, (int(x1), int(y1 + 3)), (int(x1 + 100), int(y1 -8)), color, -1)
            cv2.putText(img, text, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1, cv2.LINE_AA)    
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        yield img
        # size = (960, 450)
        # img = cv2.resize(img, size)

def process_video(video_path, cfg, predictor, model):
    outputfile = "processed_" + video_path.replace('mp4', '') + "webm"


    frameno = 0
    bulk = False
    batch_size = 16
    imgs = []
    global video_writer
    video_writer = None
    cap = cv2.VideoCapture(video_path)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if not video_writer:
            height, width, _ = frame.shape
            video_writer = cv2.VideoWriter(outputfile, cv2.VideoWriter_fourcc(*'vp80'), 25, (width, height))
            
        if frame is None:
            if len(imgs) > 1:
                outputs = process_bulk_frames(frameno, imgs)
                imgs = list(compute_final_frame(imgs, outputs, frameno, outputfile))
                for img in imgs:
                    video_writer.write(img)
            break

        frameno += 1
        img = frame

        if bulk:
            imgs.append(img)
            if len(imgs) == batch_size:
                outputs = process_bulk_frames(frameno, imgs)
                imgs = list(compute_final_frame(imgs, outputs, frameno, outputfile))
                if img in imgs:
                    video_writer.write(imgs[0])                
                imgs = []
        else:
            outputs = process_single_frame(frameno, img, predictor)
            imgs = list(compute_final_frame([img], [outputs], frameno, outputfile))
            video_writer.write(imgs[0])
    video_writer.release()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print('python detect.py video_path')
        exit()
    video_path = sys.argv[1]
    cfg, predictor, model = load_models()
    print_total_frames(video_path)
    process_video(video_path, cfg, predictor, model)
