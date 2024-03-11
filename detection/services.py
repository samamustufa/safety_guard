# services.py

import os
import uuid
from ultralytics import YOLO
import cv2

def process_video(input_video_path, output_folder, model_paths):
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print("Error: Unable to open the video file.")
        return False, [], {}

    H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    success_flags = []
    output_filenames = []
    counts = {'HELMET': 0, 'NOHELMET': 0, 'VEST': 0, 'NOVEST': 0}

    temp_output_path = os.path.join(output_folder, 'temp_output.mp4')
    temp_output = cv2.VideoWriter(temp_output_path, cv2.VideoWriter_fourcc(*'avc1'), fps, (W, H))

    models = [YOLO(path) for path in model_paths]
    thresholds = [0.5] * len(models)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        for model, threshold in zip(models, thresholds):
            results = model(frame)[0]

            for result in results.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = result

                if score > threshold:
                    class_name = results.names[int(class_id)].upper()

                    if class_name in counts:
                        counts[class_name] += 1

                    if class_name in ['HELMET', 'NOHELMET']:
                        color = (0, 255, 0) if class_name == 'HELMET' else (0, 0, 255)
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 4)
                        cv2.putText(frame, class_name, (int(x1), int(y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 1.3, color, 3, cv2.LINE_AA)

                    elif class_name in ['VEST', 'NOVEST']:
                        color = (255, 0, 0) if class_name == 'VEST' else (0, 0, 255)
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 4)
                        cv2.putText(frame, class_name, (int(x1), int(y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 1.3, color, 3, cv2.LINE_AA)

        temp_output.write(frame)

    temp_output.release()

    output_filename = 'output-' + str(uuid.uuid4()) + '.mp4'
    output_video_path = os.path.join(output_folder, output_filename)
    os.rename(temp_output_path, output_video_path)

    cap.release()
    cv2.destroyAllWindows()

    return True, [output_filename], counts
