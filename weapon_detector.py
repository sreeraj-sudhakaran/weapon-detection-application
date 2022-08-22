import os
import sys
from pathlib import Path
import torch
import torch.backends.cudnn as cudnn

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from models.common import DetectMultiBackend
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device
from utils.general import increment_path,check_img_size,non_max_suppression,scale_coords,cv2
from utils.dataloaders import LoadImages_direct

def find_weapon_init():
    
    global model,stride, names, pt,imgsz,device
    data=r'data\coco128.yaml'
    weights=['runs/content/exp/best.pt']
    source=r'C:\Users\sreer\Desktop\opencv_examplé\yolov5\contents\demo.jpg'
    device = select_device('')
    half=False
    device=''
    
    
    imgsz=[640,640]

    name='exp'
    exist_ok=False
    project=ROOT / 'runs/detect'

    save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run
    
    # Load model
    device = select_device(device)
    model = DetectMultiBackend(weights, device=device, dnn=False, data=data, fp16=half)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)  # check image size


def find_weapon_check(pic_data, label_list):
    weapon_detection_flag=0
    conf_thres=0.25
    iou_thres=0.45
    classes=None
    agnostic_nms=False
    max_det=1000
    line_thickness=3
    box_ok=0
    #print(time_sync())

    label_detect = [0] * len(label_list)
    
    source = pic_data
    dataset = LoadImages_direct(source, img_size=imgsz, stride=stride, auto=pt)
    bs = 1  # batch_size
    #print('inference')
    # Run inference
    model.warmup(imgsz=(1 if pt else bs, 3, *imgsz))  # warmup
    seen, windows, dt = 0, [], [0.0, 0.0, 0.0]
    for path, im, im0s, vid_cap, s in dataset:
        im = torch.from_numpy(im).to(device)
        im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim
        # Inference
        visualize = False
        pred = model(im, augment=False, visualize=False)
        # NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
        # Process predictions
        for i, det in enumerate(pred):  # per image
            seen += 1
            im0, frame = im0s.copy(), getattr(dataset, 'frame', 0)
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            imc = im0  # for save_crop
            annotator = Annotator(im0, line_width=line_thickness, example=str(names))
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()
                # Print results
                for c in det[:, -1].unique():
                    weapon_detection_flag = (det[:, -1] == c).sum()  # detections per class
                # Write results
                for *xyxy, conf, cls in reversed(det):
                    if True :  # Add bbox to image
                        c = int(cls)  # integer class
                        label = (f'{names[c]} {conf:.2f}')
                        print(label)                                                                                ##label name
                        for i in range(0,len(label_list)):
                            if(label_list[i] in label):
                                label_detect[i]=1
                                box_ok = 1
                            #else:
                                #print("qwe"+label_list[i]+label+"qwer")
                            if box_ok==1:
                                annotator.box_label(xyxy, label, color=colors(c, True))
                        
            im0 = annotator.result()
            cv2.waitKey(0)
    #print("number=",label_detect)
    return im0,label_detect
