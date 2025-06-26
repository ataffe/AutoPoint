import cv2
import json

# @title Dynamic Programming Algorithm {form-width: "25%"}

class AnnotatedVideo:
    def __init__(self):
        self.frames = {}
        self.path = ''

    def get_last_frame_num(self):
        if not self.frames:
            return None
        return max(self.frames.keys())

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