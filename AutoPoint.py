from random import randint
from AnnotatedVideo import AnnotatedVideo
from OpticalFlow import get_optical_flows
from Interpolate import interpolate
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
        if frame_num == 0:
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
        else:
            color = ant.get_points(0)[0][-1]
        ant.add_point(frame_num, (x, y, color))
        cv2.circle(img, (x, y), 5, color, -1)
        cv2.putText(img, str(ant.num_points(frame_num)), (x + 5, y + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1,
                    cv2.LINE_AA)

def get_point(frame, frame_num, window_name, ant):
    cv2.setMouseCallback(window_name, mouse_callback, (ant, frame, frame_num))
    cv2.imshow(window_name, frame)
    cv2.waitKey(0)


"""
Prompts the user to select start and end points in the first and last frames of a video.
Returns an AnnotatedVideo object containing the selected points.
"""
def get_start_end_point(path):
    video = cv2.VideoCapture(path)
    cv2.namedWindow("AutoPoint")
    annotation = AnnotatedVideo()
    num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    if video.isOpened():
        print("Select point to track in frame 1")
        success, frame = video.read()
        if not success:
            raise RuntimeError("Cannot read video file")
        get_point(frame, 0, "AutoPoint", annotation)
        video.set(cv2.CAP_PROP_POS_FRAMES, num_frames - 1)
        print("Select point to track in last frame")
        success, frame = video.read()
        if not success:
            raise RuntimeError("Cannot read video file")
        get_point(frame, num_frames - 1, "AutoPoint", annotation)
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
    video.release()
    cv2.destroyAllWindows()
    return annotation

def run_autopoint(path, optical_flows, device="cpu"):
    annotation = get_start_end_point(path)
    color = annotation.get_points(0)[0][-1]  # Get color from the first point
    first_point = annotation.get_points(0)[0][:-1]  # Exclude color
    if first_point is None:
        raise ValueError("No point selected in the first frame.")
    last_frame_num = annotation.get_last_frame_num()
    last_point = annotation.get_points(last_frame_num)[0][:-1]  # Exclude color
    if last_point is None:
        raise ValueError("No point selected in the last frame.")
    print("Estimating track using optical flow...")
    points, _ = interpolate(optical_flows, 0, first_point, last_frame_num, last_point, device=device)

    annotation = AnnotatedVideo()
    for point in points:
        annotation.add_frame_with_points([(int(point[0]), int(point[1]), color)])

    video = cv2.VideoCapture(path)
    frame_num = 0
    cv2.namedWindow("AutoPoint")
    print("Press 'q' to save and quit, 'Right Arrow' to go to next frame, 'Left Arrow' to go back")
    success, frame = video.read()
    if not success:
        raise RuntimeError("Error reading video file")

    while video.isOpened():
        points = annotation.get_points(frame_num)
        for point in points:
            x, y, color = point
            frame = cv2.circle(frame, (int(x), int(y)), 5, color, -1)

        cv2.imshow("AutoPoint", frame)
        key = cv2.waitKey(0)
        if key & 0xFF == ord('q'):
            filename = path.split("/")[-1]
            annotation.save_json(filename.split(".")[0] + ".json")
            break
        elif key == 83: # Right arrow key
            if frame_num < last_frame_num:
                frame_num += 1
                success, frame = video.read()
                if not success:
                    raise RuntimeError("Error reading video file")
        elif key == 81: # Left arrow key
            frame_num = max(0, frame_num - 1)
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            success, frame = video.read()
            if not success:
                raise RuntimeError("Error reading video file")


if __name__ == "__main__":
    device = "cpu"
    if torch.cuda.is_available():
        device = "cuda"
    elif torch.backends.mps.is_available() and torch.backends.mps.is_built():
        device = "mps"
    print(f"Using device: {device}")

    video_path = 'videos/horsejump-high.mp4'
    optical_flows = get_optical_flows(video_path, device)
    run_autopoint(video_path, optical_flows, device)
    # print(optical_flows.shape)
    # start_annotation(video_path)
