from typing import Tuple
import numpy as np
from scipy.spatial.qhull import QhullError
from scipy.spatial import ConvexHull
from scipy.spatial.distance import cdist
import pandas as pd
from simba.mixins.geometry_mixin import GeometryMixin
from simba.plotting.geometry_plotter import GeometryPlotter
from hmmlearn import hmm
from scipy.signal import medfilt
import cv2
from simba.utils.read_write import read_img_batch_from_video


def compute_optical_flow(frames: np.ndarray) -> list:
    """
    Compute optical flow for each pair of consecutive frames in the image stack.

    :param frames: A numpy array of shape (T, H, W) representing the stack of frames.
    :return: A list of optical flow for each pair of consecutive frames.
    """
    optical_flows = []
    T, H, W = frames.shape  # Number of frames, height, width

    for i in range(1, T):
        print(i)
        # Calculate optical flow between consecutive frames
        flow = cv2.calcOpticalFlowFarneback(frames[i - 1], frames[i], None, 0.5, 3, 15, 3, 5, 1.2, 0)
        optical_flows.append(flow)

    return optical_flows


def find_head_tail_using_optical_flow(vertices: np.ndarray, optical_flow: list) -> tuple:
    """
    Identify head and tail positions based solely on optical flow.

    :param vertices: A numpy array of shape (T, N, 2), where T is the number of frames,
                     N is the number of points per frame, and 2 represents the (x, y) coordinates of each point.
    :param optical_flow: A list of optical flow arrays for each pair of consecutive frames.
    :return: anterior (head positions) and posterior (tail positions) arrays.
    """
    T, N, _ = vertices.shape  # T = frames, N = points per frame
    anterior = np.full((T, 2), -1, dtype=np.float32)  # Head positions
    posterior = np.full((T, 2), -1, dtype=np.float32)  # Tail positions

    for i in range(1, T):
        flow = optical_flow[i - 1]  # Optical flow between the i-1 and i frame

        # Compute the motion of each point based on the optical flow
        motion_vectors = []
        for point in vertices[i - 1]:  # Each point in the previous frame
            x, y = point
            flow_vector = flow[int(y), int(x)]  # Get the flow vector at the point's (x, y)
            motion_vectors.append(flow_vector)

        motion_vectors = np.array(motion_vectors)  # Convert to numpy array

        # Compute the magnitude of the motion for each point (i.e., how much the point moved)
        movement_magnitudes = np.linalg.norm(motion_vectors, axis=1)

        # Head will be the point with the highest magnitude of motion, and tail will be the lowest
        head_idx = np.argmax(movement_magnitudes)
        tail_idx = np.argmin(movement_magnitudes)

        anterior[i] = vertices[i][head_idx]  # Set head position
        posterior[i] = vertices[i][tail_idx]  # Set tail position

    return anterior, posterior

DATA_PATH = r"D:\FST_ABOVE\data\2.csv"
VIDEO_PATH = r"D:\FST_ABOVE\2.mp4"


img = read_img_batch_from_video(video_path=VIDEO_PATH, greyscale=True)
imgs = np.stack(list(img.values()))

optical_flow = compute_optical_flow(frames=imgs)

# df = pd.read_csv(DATA_PATH, index_col=0)
# vertice_cols = [x for x in df.columns if 'vertice' in x]
# data_arr = df[vertice_cols].values.reshape(len(df), int(len(vertice_cols)/2), 2)
# anterior, posterior = find_head_tail_using_optical_flow(vertices=data_arr, optical_flow=optical_flow)
#
# anterior_points = GeometryMixin.bodyparts_to_points(data=anterior)
# posterior_points = GeometryMixin.bodyparts_to_points(data=posterior)
#
# plotter = GeometryPlotter(geometries=[anterior_points, posterior_points], video_name=VIDEO_PATH, palette='jet', save_dir=r"D:\FST_ABOVE\anterior_posterior", shape_opacity=1.0)
# plotter.run()