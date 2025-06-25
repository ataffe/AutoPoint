import torch
import numpy as np
import gc
import cv2
from OpticalFlow import get_optical_flows
from tqdm import tqdm


def interpolate(flows, frame1, click1, frame2, click2, radius=20, device='cpu'):
    x1, y1 = click1
    x2, y2 = click2

    # window = 41
    window = 2 * radius + 1

    # Creates a mesh grid -20, -19, ... 0 ..., 19, 20
    x, y = np.meshgrid(np.arange(-radius, radius + 1), np.arange(-radius, radius + 1))
    # Not sure why this is done, but it creates a 2D array of offsets
    offset_cost = np.stack([x, y], axis=-1)
    offset_cost = torch.tensor(offset_cost).to(device)

    # 49 x 480 x 768
    num_frames, height, width = flows.shape[0:3]

    # i: (50 x 480 x 768) = 0
    forward_i = np.zeros((num_frames + 1, height, width), dtype=np.int32)
    # j: (50 x 480 x 768) = 0
    forward_j = np.zeros((num_frames + 1, height, width), dtype=np.int32)

    # (480 x 768) = 1e10
    forward_cost = torch.ones((height, width)).to(device) * 1e10
    # First point = 0
    forward_cost[y1, x1] = 0

    # From starting frame to ending frame
    for t in tqdm(range(frame1, frame2)):
        # Pad forward cost on all sides by radius
        cost_pad = torch.nn.functional.pad(forward_cost, (radius, radius, radius, radius), 'constant', value=1e10)

        # ---------------------------------------
        # Honestly I don't understand this part starting here...
        # ---------------------------------------
        # Slice the cost tensor into patches of size (window, window) ?
        cost_unfold = cost_pad.unfold(0, window, 1).unfold(1, window, 1)
        del cost_pad
        gc.collect()
        torch.cuda.empty_cache()

        flow_cuda = torch.tensor(flows[t]).to(device)
        # Pad the flow tensor on all sides by radius
        flow_pad = torch.nn.functional.pad(flow_cuda, (0, 0, radius, radius, radius, radius), 'constant', value=1e10)
        # Slice the flow tensor into patches of size (window, window, 2) ??
        flow_unfold = flow_pad.unfold(0, window, 1).unfold(1, window, 1).permute(0, 1, 3, 4, 2)
        del flow_cuda, flow_pad
        gc.collect()
        torch.cuda.empty_cache()

        # Calculate the cost by adding the unfolded cost and the absolute difference between the unfolded flow and the offset cost
        cost = cost_unfold + torch.abs(-offset_cost[None, None] - flow_unfold).sum(axis=-1)
        cost = cost.reshape(height, width, -1)
        forward_cost, argmin_indices = torch.min(cost, axis=-1)
        del cost
        gc.collect()
        torch.cuda.empty_cache()
        # ---------------------------------------
        # End of the part I don't understand
        # ---------------------------------------

        argmin_indices = argmin_indices.cpu().numpy()
        forward_i_min, forward_j_min = argmin_indices // (window), argmin_indices % (window)
        forward_i[t] = forward_i_min + np.arange(height)[:, None] - radius
        forward_j[t] = forward_j_min + np.arange(width)[None] - radius

    # Get the last frame's cost at the click2 position
    last_cost = torch.ones((height, width)).to(device) * 1e10
    last_cost[y2, x2] = 0
    forward_cost += last_cost
    min_cost = torch.min(forward_cost).cpu().numpy()

    # Get the indices of the minimum cost in the last frame
    # Which is the last frame's cost at the click2 position
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


def test_interpolate():
    device = "cpu"
    if torch.cuda.is_available():
        device = "cuda"
    elif torch.backends.mps.is_available() and torch.backends.mps.is_built():
        device = "mps"
    video_path = 'videos/horsejump-high.mp4'
    optical_flows = get_optical_flows(video_path, device)
    video = cv2.VideoCapture(video_path)
    video_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    video_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    success, frame1 = video.read()
    assert success, "Failed to read the first frame from the video."
    video.set(cv2.CAP_PROP_POS_FRAMES, 25)
    success, frame2 = video.read()
    assert success, "Failed to read the second frame from the video."
    point1 = (video_height // 2, video_width // 2)
    point2 = (video_height // 2 + 50, video_width // 2 + 50)
    min_ij, min_cost = interpolate(optical_flows, 0, point1, 25, point2, 20, device)
    print("Interpolated points:", min_ij)
    video.release()


if __name__ == "__main__":
    test_interpolate()
