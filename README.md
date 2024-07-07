# YOLO-CSL
# Detection of objects in satellite and aerial imagery using channel and  spatially attentive YOLO-CSL for surveillance

A novel lightweight Rotational Object Detection algorithm is proposed to overcome the shortcomings of conventional computer-vision-aided object detection methods used in Remote Sensing and Surveillance that overlook the variability in size and orientation of objects in satellite and aerial images. This advanced algorithm  integrates a branch dedicated to angle prediction and employs the circular smooth label (CSL) method for angle  classification. This approach is suitable for scenarios that require detection in rotational boxes. Our work is  further distinguished by the introduction of a novel Channel and Spatial Attention (CSA) module, which is  seamlessly integrated into the YOLOv5-CSL framework via the C3CS module. This module accentuates pertinent  features through both the channel and spatial attention mechanisms. In addition, bicubic interpolation and the GELU activation function were incorporated into the YOLOv5-CSLA model. Our model achieved 57.86 mAP on  the challenging DOTA v2 dataset surpassing the second-best method by 0.20 points and simultaneously consuming 11 million fewer parameters and 103 fewer GFLOPs (our model consumes 25 M Params and 54  GFLOPs), justifying its suitability for deployment on a large majority of platforms, as the compute required is a challenge in real-time deployment scenarios.

This repository is based on [OBB-YOLO](https://github.com/hukaixuan19970627/yolov5_obb).

# Paper Citation-
```
@article{chaurasia2024detection,
  title={Detection of objects in satellite and aerial imagery using channel and spatially attentive YOLO-CSL for surveillance},
  author={Chaurasia, Divyansh and Patro, BDK},
  journal={Image and Vision Computing},
  volume={147},
  pages={105070},
  year={2024},
  publisher={Elsevier}
}
```



# Getting Started 

For installation instructions, please see [install.md](./install.md).

# Train a model

**1. Prepare custom dataset files**

1.1 Make sure the labels format is [poly classname diffcult], e.g., You can set **diffcult=0**
```
  x1      y1       x2        y2       x3       y3       x4       y4       classname     diffcult

1686.0   1517.0   1695.0   1511.0   1711.0   1535.0   1700.0   1541.0   large-vehicle      1
```
![image](https://user-images.githubusercontent.com/72599120/159213229-b7c2fc5c-b140-4f10-9af8-2cbc405b0cd3.png)


1.2 Split the dataset. 
```shell
cd yolov5_obb
python DOTA_devkit/ImgSplit_multi_process.py
```
or Use the orignal dataset. 
```shell
cd yolov5_obb
```

1.3 Make sure your dataset structure same as:
```
parent
├── yolov5
└── datasets
    └── DOTAv1.5
        ├── train_split_rate1.0_subsize1024_gap200
        ├── val_split_rate1.0_subsize1024_gap200
        └── test_split_rate1.0_subsize1024_gap200
            ├── images
                 |────1.jpg
                 |────...
                 └────10000.jpg
            ├── labelTxt
                 |────1.txt
                 |────...
                 └────10000.txt

```

**Note:**
* DOTA is a high resolution image dataset, so it needs to be splited before training/testing to get better performance.

**2. Train**

2.1 Train with specified GPUs. (for example with GPU=3)

```shell
python train.py --device 3
```

2.2 Train with multiple(4) GPUs. (DDP Mode)

```shell
python -m torch.distributed.launch --nproc_per_node 4 train.py --device 0,1,2,3
```

2.3 Train the orignal dataset demo.
```shell
python train.py \
  --weights 'weights/yolov5n_s_m_l_x.pt' \
  --data 'data/yolov5obb_demo.yaml' \
  --hyp 'data/hyps/obb/hyp.finetune_dota.yaml' \
  --epochs 10 \
  --batch-size 1 \
  --img 1024 \
  --device 0
```

2.4 Train the splited dataset demo.
```shell
python train.py \
  --weights 'weights/yolov5n_s_m_l_x.pt' \
  --data 'data/yolov5obb_demo_split.yaml' \
  --hyp 'data/hyps/obb/hyp.finetune_dota.yaml' \
  --epochs 10 \
  --batch-size 2 \
  --img 1024 \
  --device 0
```

# Inferenece with pretrained models. (Splited Dataset)
This repo provides the validation/testing scripts to evaluate the trained model.

Examples:

Assume that you have already downloaded the checkpoints to `runs/train/yolov5m_csl_dotav1.5/weights`.

1. Test yolov5-obb with single GPU. Get the HBB metrics.

```shell
python val.py \
 --data 'data/yolov5obb_demo_split.yaml' \
 --weights 'runs/train/yolov5m_csl_dotav1.5/weights/best.pt' \
 --batch-size 2 --img 1024 --task 'val' --device 0 --save-json --name 'obb_demo_split'

               Class     Images     Labels          P          R     mAP@.5 mAP@.5:.95: 100%|██████████| 3/3 [00:02<00:00,  1.09it/s]                                        
                 all          6         68      0.921      0.914      0.966      0.776
               plane          6         16      0.946          1      0.995      0.934
       small-vehicle          6         35      0.928      0.741      0.916      0.599
       large-vehicle          6         17       0.89          1      0.986      0.793
Speed: .................................................... per image at shape (2, 3, 1024, 1024)
...
Evaluating pycocotools mAP... saving runs/val/obb_demo_split/best_obb_predictions.json...
---------------------The hbb and obb results has been saved in json file-----------------------
```

2. Parse the results. Get the poly format results.
```shell 
python tools/TestJson2VocClassTxt.py --json_path 'runs/val/obb_demo_split/best_obb_predictions.json' --save_path 'runs/val/obb_demo_split/obb_predictions_Txt'
``` 

3. Merge the results. (If you split your dataset)
```shell
python DOTA_devkit/ResultMerge_multi_process.py \
    --scrpath 'runs/val/obb_demo_split/obb_predictions_Txt' \
    --dstpath 'runs/val/obb_demo_split/obb_predictions_Txt_Merged'
```

4. Get the OBB metrics
```shell
python DOTA_devkit/dota_evaluation_task1.py \
    --detpath 'runs/val/obb_demo_split/obb_predictions_Txt_Merged/Task1_{:s}.txt' \
    --annopath 'dataset/dataset_demo/labelTxt/{:s}.txt' \
    --imagesetfile 'dataset/dataset_demo/imgnamefile.txt'

...
map: 0.6666666666666669
classaps:  [100.   0. 100.]
```

# Inferenece with pretrained models. (Original Dataset)
We provide the validation/testing scripts to evaluate the trained model.

Examples:

Assume that you have already downloaded the checkpoints to `runs/train/yolov5m_csl_dotav1.5/weights`.

1. Test yolov5-obb with single GPU. Get the HBB metrics.

```shell
python val.py \
 --data 'data/yolov5obb_demo.yaml' \
 --weights 'runs/train/yolov5m_csl_dotav1.5/weights/best.pt' \
 --batch-size 1 --img 2048 --task 'val' --device 0 --save-json --name 'obb_demo'

               Class     Images     Labels          P          R     mAP@.5 mAP@.5:.95: 100%|██████████| 1/1 [00:00<00:00,  1.98it/s]                                        
                 all          1         56       0.97       0.85      0.953      0.752
               plane          1         11          1          1      0.995      0.944
       small-vehicle          1         34          1      0.641      0.889      0.535
       large-vehicle          1         11       0.91      0.909      0.976      0.777
Speed: .................................................... per image at shape (1, 3, 2048, 2048)
...
Evaluating pycocotools mAP... saving runs/val/obb_demo/best_obb_predictions.json...
---------------------The hbb and obb results has been saved in json file-----------------------
```

2. Parse the results. Get the poly format results.
```shell 
python tools/TestJson2VocClassTxt.py --json_path 'runs/val/obb_demo/best_obb_predictions.json' --save_path 'runs/val/obb_demo/obb_predictions_Txt'
``` 

3. Get the OBB metrics
```shell
python DOTA_devkit/dota_evaluation_task1.py \
    --detpath 'runs/val/obb_demo/obb_predictions_Txt/Task1_{:s}.txt' \
    --annopath 'dataset/dataset_demo/labelTxt/{:s}.txt' \
    --imagesetfile 'dataset/dataset_demo/imgnamefile.txt'

...
map: 0.6666666666666669
classaps:  [100.   0. 100.]
```

# Run inference on images, videos, directories, streams, etc. Then save the detection file.
1. image demo
```shell
python detect.py --weights 'runs/train/yolov5m_csl_dotav1.5/weights/best.pt' \
  --source 'dataset/dataset_demo/images/' \
  --img 2048 --device 0 --conf-thres 0.25 --iou-thres 0.2 --hide-labels --hide-conf
```

***If you want to evaluate the result on DOTA test-dev, please zip the poly format results files and submit it to the  [evaluation server](https://captain-whu.github.io/DOTA/index.html).**
