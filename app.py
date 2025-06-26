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
import time
from AnnotatedVideo import AnnotatedVideo

device = 'cuda' if torch.cuda.is_available() else 'cpu'
# ===================================================
# ================ 1. LOGIC CODE ====================
# ===================================================

# (Your logic code here)

# ===================================================
# ============== 2. EVENT BINDINGS ==================
# ===================================================

def handle_file_selection(file_path, ui, ant_video=None):
    print("File selected:", file_path)
    ui['pages'].set_current_page(1)  # Switch to page 1 after file selection
    ant_video.path = file_path

def run_optical_flow(prev, next, ant, ui):
    global device
    torch.set_grad_enabled(False)
    raft = raft_large(weights=Raft_Large_Weights.DEFAULT, progress=False).to(device)
    raft = raft.eval()

    video = cv2.VideoCapture(ant.path)
    flows = []
    first_frame = True
    frame1 = None
    while video.isOpened():
        if first_frame:
            success, frame1 = video.read()
            frame1 = cv2.resize(frame1, (768, 480))
            frame1 = np.array(frame1).astype(np.float32) / 127.5 - 1.0
            frame1 = frame1.transpose(2, 0, 1)[None]
            if not success:
                print("Unable to read first frame")
                break

        success, frame2 = video.read()
        if not success:
            print("Unable to read frame")
            break

        if frame1 is None:
            print("Unable to read first frame")
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
        ui['page_1']['optical_flow_image'].image = color_flow
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame1 = frame2

        if first_frame:
            first_frame = False

    flows = np.stack(flows)
    del raft
    gc.collect()
    torch.cuda.empty_cache()
    print(flows.shape)
    print(np.abs(flows).max())
    video.release()
    cv2.destroyAllWindows()

def attach_events(ui):
    """
    Bind events to UI components.
    :param ui: Dictionary containing UI components.
    """
    annotation = AnnotatedVideo()
    ui['pages'].animation_duration = 250 # ms
    ui['page_0']['file_selector'].on_file_selected = partial(handle_file_selection, ui=ui, ant_video=annotation)
    ui['pages'].on_page_change = partial(run_optical_flow, ant=annotation, ui=ui)

# ===================================================
# ============== 3. MAIN FUNCTION ==================
# ===================================================


def main():
    app = pv.PvApp()
    ui = create_ui()
    attach_events(ui)
    ui["window"].show()
    app.run()


if __name__ == '__main__':
    main()
