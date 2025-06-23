from random import randint
from AnnotatedVideo import AnnotatedVideo
from OpticalFlow import get_optical_flows
import cv2
import numpy as np
import torch

def draw_dashed_line(img, pt1, pt2, color, thickness=1, dash_length=10, gap_length=5):
    # Compute the line vector
    dist = np.linalg.norm(np.array(pt2) - np.array(pt1))
    if dist == 0:
        return  # Same point, do nothing

    # Unit vector in the direction of the line
    line_vector = (np.array(pt2) - np.array(pt1)) / dist
    # Current point on the line
    current_pt = np.array(pt1, dtype=np.float32)

    # Draw dashes
    while np.linalg.norm(current_pt - np.array(pt1)) < dist:
        next_pt = current_pt + line_vector * dash_length
        if np.linalg.norm(next_pt - np.array(pt1)) > dist:
            next_pt = np.array(pt2)

        cv2.line(img,
                 tuple(np.round(current_pt).astype(int)),
                 tuple(np.round(next_pt).astype(int)),
                 color, thickness)
        current_pt = next_pt + line_vector * gap_length


def mouse_callback(event, x, y, flags, param):
    ant, img, frame_num = param
    if event == cv2.EVENT_MOUSEMOVE:
        img_copy = img.copy()
        img_width = img.shape[1]
        img_height = img.shape[0]
        draw_dashed_line(img_copy, (x, 0), (x, y), (0, 0, 0), 2)
        draw_dashed_line(img_copy, (x, y), (x, img_height), (0, 0, 0), 2)
        draw_dashed_line(img_copy, (0, y), (x, y), (0, 0, 0), 2)
        draw_dashed_line(img_copy, (x, y), (img_width, y), (0, 0, 0), 2)
        cv2.circle(img_copy, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow('AutoPoint', img_copy)
    elif event == cv2.EVENT_LBUTTONDOWN:
        color = (randint(0, 255), randint(0, 255), randint(0, 255))
        ant.add_point(frame_num, (x, y, color))
        cv2.circle(img, (x, y), 5, color, -1)
        cv2.putText(img, str(ant.num_points(frame_num)), (x + 5, y + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1,
                    cv2.LINE_AA)


def start_annotation(path):
    video = cv2.VideoCapture(path)
    cv2.namedWindow("AutoPoint")
    annotation = AnnotatedVideo()
    frame_num = 0
    frames = []
    first_frame = True
    while video.isOpened():
        success, frame = video.read()
        if not success:
            break
        if first_frame:
            annotation.add_frame()
            first_frame = False
        else:
            annotation.add_frame_with_points(annotation.get_points(frame_num - 1))
            frame = annotation.draw_points(frame, frame_num)

        cv2.setMouseCallback("AutoPoint", mouse_callback, (annotation, frame, frame_num))
        cv2.imshow("AutoPoint", frame)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            annotation.save_json("autopoint.json")
            break
        frames.append(frame)
        frame_num += 1


if __name__ == "__main__":
    device = "cpu"
    if torch.cuda.is_available():
        device = "cuda"
    elif torch.backends.mps.is_available() and torch.backends.mps.is_built():
        device = "mps"
    print(f"Using device: {device}")

    video_path = 'videos/horsejump-high.mp4'
    optical_flows = get_optical_flows(video_path, device)
    print(optical_flows.shape)
    # start_annotation(video_path)
