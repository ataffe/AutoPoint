import pyvisual as pv
from ui.ui import create_ui
from functools import partial
from torchvision.models.optical_flow import raft_large
from torchvision.models.optical_flow import Raft_Large_Weights
import cv2
import gc
import flow_vis
import numpy as np
import torch
from OpticalFlowVideo import OpticalFlowVideo
import time

device = 'cuda' if torch.cuda.is_available() else 'cpu'
raft = raft_large(weights=Raft_Large_Weights.DEFAULT, progress=False).to(device)
raft = raft.eval()

# ===================================================
# ================ 1. LOGIC CODE ====================
# ===================================================

# (Your logic code here)

# ===================================================
# ============== 2. EVENT BINDINGS ==================
# ===================================================

def handle_file_selection(file_path, ui, opt_flow_vid=None):
    print("File selected:", file_path)
    ui['pages'].set_current_page(1)  # Switch to page 1 after file selection
    opt_flow_vid.video_path = file_path
    ui['page_1']['optical_flow_video'].video_path = file_path
    ui['page_1']['optical_flow_video'].start()
    ui['page_1']['optical_flow_video'].frame_processor = partial(process_optical_flow_frame, opt_flow_vid=opt_flow_vid)


def process_optical_flow_frame(frame, opt_flow_vid):

    if len(opt_flow_vid.frames) == 0:
        frame_data = frame.copy()
        frame_data = cv2.resize(frame_data, (768, 480))
        frame_data = np.array(frame_data).astype(np.float32) / 127.5 - 1.0
        frame_data = frame_data.transpose(2, 0, 1)[None]
        opt_flow_vid.frames.append(frame_data)
    else:
        frame = cv2.resize(frame, (768, 480))
        frame = np.array(frame).astype(np.float32) / 127.5 - 1.0
        frame = frame.transpose(2, 0, 1)[None]
        last_frame = opt_flow_vid.frames[-1]
        opt_flow_vid.frames.append(frame)
        flow = raft(torch.tensor(last_frame).to(device), torch.tensor(frame).to(device))
        flow = flow[-1][0].cpu().detach().numpy()
        flow = flow.transpose(1, 2, 0)
        opt_flow_vid.optical_flows.append(flow)
        frame = flow_vis.flow_to_color(flow)
    return frame


def attach_events(ui):
    """
    Bind events to UI components.
    :param ui: Dictionary containing UI components.
    """
    optical_flow_video = OpticalFlowVideo()
    ui['pages'].animation_duration = 250 # ms
    ui['page_0']['file_selector'].on_file_selected = partial(handle_file_selection, ui=ui, opt_flow_vid=optical_flow_video)
    # ui['page_1']['optical_flow_video'].frame_processor = partial(process_optical_flow_frame, opt_flow_vid=optical_flow_video)

# ===================================================
# ============== 3. MAIN FUNCTION ==================
# ===================================================


def main():
    torch.set_grad_enabled(False)
    app = pv.PvApp()
    ui = create_ui()
    attach_events(ui)
    ui["window"].show()
    app.run()


if __name__ == '__main__':
    main()
