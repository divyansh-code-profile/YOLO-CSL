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

# Dataset Used - [DOTA v2](https://captain-whu.github.io/DOTA/dataset.html).
# For setting up refer to [GetStart.md](./docs/GetStart.md).
