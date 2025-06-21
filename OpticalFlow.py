import torch
from tqdm import tqdm
from torchvision.models.optical_flow import raft_large
from torchvision.models.optical_flow import Raft_Large_Weights
import cv2
import gc
import flow_vis
import numpy as np

def get_optical_flows(video_path):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch.set_grad_enabled(False)

    raft = raft_large(weights=Raft_Large_Weights.DEFAULT, progress=False).to(device)
    raft = raft.eval()

    video = cv2.VideoCapture(video_path)
    flows = []
    first_frame = True
    with tqdm(total=video.get(cv2.CAP_PROP_FRAME_COUNT)) as pbar:
        while video.isOpened():
            if first_frame:
                ret1, frame1 = video.read()
                frame1 = cv2.resize(frame1, (768, 480))
                frame1 = np.array(frame1).astype(np.float32) / 127.5 - 1.0
                frame1 = frame1.transpose(2, 0, 1)[None]

            ret2, frame2 = video.read()
            if not ret1 or not ret2:
                break

            # Resize, normalize, then transpose h, w, c -> b, c, h, w
            frame2 = cv2.resize(frame2, (768, 480))
            frame2 = np.array(frame2).astype(np.float32) / 127.5 - 1.0
            frame2 = frame2.transpose(2, 0, 1)[None]

            flow = raft(torch.tensor(frame1).to(device), torch.tensor(frame2).to(device))
            flow = flow[-1][0].cpu().numpy()
            flow = flow.transpose(1, 2, 0)
            flows.append(flow)

            color_flow = flow_vis.flow_to_color(flow)
            cv2.imshow('flow', color_flow)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            frame1 = frame2
            pbar.update(1)

            if first_frame:
                pbar.update(1)
                first_frame = False

    flows = np.stack(flows)
    del raft
    gc.collect()
    torch.cuda.empty_cache()
    print(flows.shape)
    print(np.abs(flows).max())
    video.release()
    cv2.destroyAllWindows()
    return flows