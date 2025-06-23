import cv2
import json
import torch
import numpy as np
import gc
from random import randint

# @title Dynamic Programming Algorithm {form-width: "25%"}

def interpolate(flows, frame1, click1, frame2, click2, radius=20):
  x1, y1 = click2idx(click1)
  x2, y2 = click2idx(click2)

  window = 2 * radius + 1
  x, y = np.meshgrid(np.arange(-radius, radius + 1), np.arange(-radius, radius + 1))
  offset_cost = np.stack([x, y], axis=-1)
  offset_cost = torch.tensor(offset_cost).to(device)

  num_frames, height, width = flows.shape[0:3]

  forward_i = np.zeros((num_frames + 1, height, width), dtype=np.int32)
  forward_j = np.zeros((num_frames + 1, height, width), dtype=np.int32)

  forward_cost = torch.ones((height, width)).to(device) * 1e10
  forward_cost[y1, x1] = 0

  for t in range(frame1, frame2):
    cost_pad = torch.nn.functional.pad(forward_cost, (radius, radius, radius, radius), 'constant', value=1e10)
    cost_unfold = cost_pad.unfold(0, window, 1).unfold(1, window, 1)
    del cost_pad
    gc.collect()
    torch.cuda.empty_cache()

    flow_cuda = torch.tensor(flows[t]).to(device)
    flow_pad = torch.nn.functional.pad(flow_cuda, (0, 0, radius, radius, radius, radius), 'constant', value=1e10)
    flow_unfold = flow_pad.unfold(0, window, 1).unfold(1, window, 1).permute(0, 1, 3, 4, 2)
    del flow_cuda, flow_pad
    gc.collect()
    torch.cuda.empty_cache()

    cost = cost_unfold + torch.abs(-offset_cost[None, None] - flow_unfold).sum(axis=-1)
    cost = cost.reshape(height, width, -1)
    forward_cost, argmin_indices = torch.min(cost, axis=-1)
    del cost
    gc.collect()
    torch.cuda.empty_cache()

    argmin_indices = argmin_indices.cpu().numpy()
    forward_i_min, forward_j_min = argmin_indices // (window), argmin_indices % (window)
    forward_i[t] = forward_i_min + np.arange(height)[:, None] - radius
    forward_j[t] = forward_j_min + np.arange(width)[None] - radius

  last_cost = torch.ones((height, width)).to(device) * 1e10
  last_cost[y2, x2] = 0
  forward_cost += last_cost
  min_cost = torch.min(forward_cost).cpu().numpy()

  argmin_indices = torch.argmin(forward_cost).item()
  min_i, min_j = argmin_indices // width, argmin_indices % width
  min_ij = [(min_j, min_i)]

  for t in range(frame2 - 1, frame1 - 1, -1):
    min_i, min_j = forward_i[t, min_i, min_j], forward_j[t, min_i, min_j]
    min_ij.insert(0, (min_j, min_i))

  del forward_cost
  gc.collect()
  torch.cuda.empty_cache()
  return np.stack(min_ij), min_cost

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