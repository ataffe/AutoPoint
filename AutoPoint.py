from random import randint

import json
import cv2
import numpy as np


class AnnotatedVideo:
    def __init__(self):
        self.frames = {}

    def add_frame(self):
        num_frames = len(self.frames)
        self.frames[num_frames] = []

    def add_frame_with_points(self, points):
        num_frames = len(self.frames.keys())
        self.frames[num_frames] = points

    def get_points(self, frame_num):
        return self.frames.get(frame_num, [])

    def add_point(self, frame_num, point):
        points = self.frames.get(frame_num, [])
        points.append(point)
        self.frames[frame_num] = points

    def num_points(self, frame_num):
        return len(self.frames[frame_num])

    def draw_points(self, frame, frame_num):
        for idx, point in enumerate(self.frames.get(frame_num, [])):
            x, y, color = point
            cv2.circle(frame, (int(x), int(y)), 5, color, -1)
            cv2.putText(frame, str(idx + 1), (x + 5, y + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),
                        1,
                        cv2.LINE_AA)
        return frame

    def save_json(self, filename):
        json_frames = {}
        for frame_num in self.frames.keys():
            points = self.frames[frame_num]
            json_frames[f"frame_{frame_num}"] = []
            for point in points:
                json_frames[f"frame_{frame_num}"].append(point[:-1])

        with open(filename, 'w') as f:
            json.dump(json_frames, f, indent=4)

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
    video_path = 'tapnet/examplar_videos/horsejump-high.mp4'
    # optical_flows = get_optical_flows(video_path)
    start_annotation(video_path)
