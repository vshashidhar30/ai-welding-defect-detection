# AI Welding Defect Detection System

An AI-based welding defect detection system developed using YOLOv8, OpenCV, Python, and Tkinter GUI for real-time industrial quality inspection.

The project focuses on detecting common welding defects from images and providing defect explanations, causes, and possible solutions through an interactive graphical interface.

---

## Features

- Detects welding defects such as:
  - Porosity
  - Spatter
  - Underfill

- YOLOv8n-based object detection
- GUI-based image selection and visualization
- Bounding box defect localization
- Defect explanation module
- Automatic result saving
- Lightweight and simple deployment workflow

---

## Technologies Used

- Python
- YOLOv8
- OpenCV
- Tkinter
- Pillow
- Ultralytics

---

## Project Workflow

1. Image Collection
2. Image Annotation using Roboflow
3. Data Augmentation
4. YOLOv8n Model Training
5. GUI Development
6. Real-time Defect Detection
7. Result Visualization and Saving

---

## Dataset Preparation

- Public welding defect images and lab images were used.
- Images were annotated using Roboflow.
- Dataset augmentation techniques included:
  - Rotation
  - Flipping
  - Brightness adjustment
  - Noise addition
  - Blur augmentation

The dataset was exported in YOLO format for training and validation.

---

## Results and Observations

- Successfully implemented a YOLOv8n-based welding defect detection workflow.
- The system was able to identify defects such as porosity, spatter, and underfill on test images.
- GUI integration enabled image selection, defect visualization, and defect explanation.
- Training graphs showed gradual reduction in training losses during model learning.
- Limited dataset size and hardware constraints affected overall model accuracy and generalization.
- The project mainly demonstrates workflow integration, defect detection pipeline creation, and practical deployment concepts.

---


## Future Improvements

- Improve dataset size and diversity
- Increase training epochs
- Add casting defect detection
- Add deep drawing defect detection
- Improve mobile deployment performance
- Add live camera-based inspection

---

## Author

Shashidhar Vegaraju
