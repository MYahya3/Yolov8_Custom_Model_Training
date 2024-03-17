from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.train(data="yolo_training/dataset.yaml", epochs=2, imgsz=320)