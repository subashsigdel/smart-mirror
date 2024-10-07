from ultralytics import YOLO

# Load the pretrained YOLOv8 nano model (or your preferred version)
model = YOLO('yolov8n.pt')

# Train the model on your dataset
model.train(data='/home/hitech/smart-mirror/ObjectDetection/datasets/data.yaml', epochs=50, batch=16, imgsz=640)
