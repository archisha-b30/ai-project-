import cv2
from ultralytics import YOLO
import numpy as np
import pandas as pd

class VehicleDetector:
    """
    Vehicle Detection Module using YOLOv8.
    Detects cars, trucks, buses, motorcycles from video frames.
    """

    def __init__(self, model_path='yolov8n.pt'):
        self.model = YOLO(model_path)
        self.vehicle_classes = ['car', 'truck', 'bus', 'motorcycle', 'ambulance']
        self.lane_regions = {
            'north': (0, 0, 320, 240),
            'south': (320, 240, 640, 480),
            'east': (320, 0, 640, 240),
            'west': (0, 240, 320, 480)
        }

    def detect_vehicles(self, frame):
        results = self.model(frame, conf=0.35)
        lane_counts = {lane: {cls: 0 for cls in self.vehicle_classes} for lane in self.lane_regions}
        total_counts = {cls: 0 for cls in self.vehicle_classes}
        boxes = []

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                cls_name = result.names[int(box.cls)]
                if cls_name not in total_counts:
                    continue
                total_counts[cls_name] += 1
                boxes.append((int(x1), int(y1), int(x2), int(y2), cls_name))
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2
                for lane, (lx1, ly1, lx2, ly2) in self.lane_regions.items():
                    if lx1 <= center_x <= lx2 and ly1 <= center_y <= ly2:
                        lane_counts[lane][cls_name] += 1
                        break

        return lane_counts, total_counts, boxes

    def draw_detections(self, frame, boxes):
        for x1, y1, x2, y2, label in boxes:
            color = (0, 255, 0) if label != 'ambulance' else (0, 0, 255)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        return frame

    def process_video(self, video_path, output_counts=False):
        cap = cv2.VideoCapture(video_path)
        history = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            lane_counts, total_counts, boxes = self.detect_vehicles(frame)
            history.append({'lane_counts': lane_counts, 'total_counts': total_counts})
            if output_counts:
                annotated = self.draw_detections(frame, boxes)
                cv2.imshow('Traffic Detection', annotated)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        cap.release()
        cv2.destroyAllWindows()
        if output_counts and history:
            records = []
            for step, snapshot in enumerate(history):
                record = {'step': step}
                record.update({f'{lane}_{cls}': count for lane, values in snapshot['lane_counts'].items() for cls, count in values.items()})
                records.append(record)
            pd.DataFrame(records).to_csv('data/vehicle_counts.csv', index=False)
        return history

    def process_webcam(self, output_counts=False):
        return self.process_video(0, output_counts=output_counts)
