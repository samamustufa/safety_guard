import cv2
import numpy as np
from shapely.geometry import Polygon
from ultralytics import YOLO
import os
import json  # Import the json module
from django.conf import settings
from .models import RestrictedAreaData
from login.models import Login

UPLOAD_FOLDER = r"D:\Users\mustufa\Desktop\django_a_file\version_1_ori\final_safetyweb\static\upload_folder"
FIRST_FRAME_FOLDER = r"D:\Users\mustufa\Desktop\django_a_file\version_1_ori\final_safetyweb\static\first_frame"
OUTPUT_FOLDER = r"D:\Users\mustufa\Desktop\django_a_file\version_1_ori\final_safetyweb\static\output_folder"

def count_persons_entered_restricted_area(video, coordinates):
    # Initialize YOLO model
    model = YOLO("yolov8n.pt")
    names = model.names
    entering_persons = {}
    # Open video for processing
    video_capture = cv2.VideoCapture(video)
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'acv1')  # MP4V codec
    output_video_path = os.path.join(OUTPUT_FOLDER, 'output_video.mp4')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (720, 480))
    # Initialize variables
    persons_entered_count = 0

    # Create a Shapely Polygon from the user-input coordinates
    restricted_area_shapely = Polygon(coordinates)

    color_restricted_entered = (255, 0, 0)  # Blue
    color_restricted_empty = (255, 255, 255)  # White
    color_person_inside = (0, 0, 255)  # Red
    color_person_outside = (0, 255, 0)  # Green

    while True:
        ret, frame = video_capture.read()

        if not ret:
            break
        frame = cv2.resize(frame, (720, 480))   
        results = model.track(frame, classes=[0], persist=True)
        # boxes = results[0].boxes
        # Draw restricted area
        cv2.polylines(frame, [np.array(coordinates)], isClosed=True, color=color_restricted_empty, thickness=2)

        for box in results[-1].boxes.data:
            class_id = int(box[5])
            # confidence = float(box.cpu().conf)
            confidence = 0
            x1, y1, x2, y2 = box[:4].cpu().numpy()

            x3, y3 = x1 + abs(x2 - x1), y1
            x4, y4 = x1, y1 + abs(y1 - y2)

            person_polygon_shapely = Polygon([(x1, y1), (x4, y4), (x2, y2), (x3, y3)])
            intersection_area = restricted_area_shapely.intersection(person_polygon_shapely).area
            union_area = restricted_area_shapely.union(person_polygon_shapely).area
            iou = intersection_area / union_area if union_area > 0 else 0

            # Check if person is inside or outside the restricted area
            if names.get(class_id) == 'person':
                person_id = int(box[4])
                if iou > 0:
                    # persons_entered_count += 1
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color_person_inside, 2)
                    cv2.putText(frame, f'Id:{person_id}', (int(x1), int(y1) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                    # Draw restricted area in blue when a person is inside
                    cv2.polylines(frame, [np.array(coordinates)], isClosed=True, color=color_restricted_entered,
                                  thickness=2)
                    
                    if person_id not in entering_persons or not entering_persons[person_id]:
                        entering_persons[person_id] = True
                        persons_entered_count += 1
                else:
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color_person_outside, 2)
                    cv2.putText(frame, f'Id:{person_id}', (int(x1), int(y1) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        # Display count of persons entered in the top-left corner
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, f'Persons Entered: {persons_entered_count}', (10, 30), font, 0.8, (0, 255, 255), 2)

        # Write the frame to the output video
        out.write(frame)
    video_capture.release()
    out.release()
    store_restricted_area_data(video, persons_entered_count)
    return persons_entered_count

from django.core.files.storage import FileSystemStorage

def store_uploaded_video(video):
    fs = FileSystemStorage(location=settings.MEDIA_ROOT)
    video_path = fs.save(video.name, video)
    return video_path


def store_restricted_area_data(video, persons_entered_count, user_id):
    try:
        # Get the video name from the path
        video_name = os.path.basename(video)

        # Create a new RestrictedAreaData instance
        restricted_area_data = RestrictedAreaData(user_id=user_id, video_name=video_name, person_count=persons_entered_count)

        # Save the instance to the database
        restricted_area_data.save()
        print("Data successfully stored in the database.")

    except Exception as e:
        print(f"Error storing data in the database: {str(e)}")

def get_first_frame(video_path):
    cap = cv2.VideoCapture(video_path)
    _, frame = cap.read()
    frame = cv2.resize(frame, (720, 480))
    frame_path = os.path.join(FIRST_FRAME_FOLDER, "first_frame.jpg")
    cv2.imwrite(frame_path, frame)
    cap.release()
    return frame_path