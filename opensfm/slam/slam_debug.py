import logging
import matplotlib.pyplot as plt
import numpy as np

from timeit import default_timer as timer
from collections import defaultdict
from opensfm import features
from opensfm import types

logger = logging.getLogger(__name__)

disable_debug = False

class AvgTimings(object):
    def __init__(self):
        self.times = defaultdict(float)
        self.n_mean = defaultdict(int)

    def addTimes(self, timings):
        for (_, (k, v, _)) in timings.items():
            self.times[k] += v
            self.n_mean[k] += 1

    def printAvgTimings(self):
        for (k, v) in self.n_mean.items():
            print("{} with {} runs: {}s".format(k, v, self.times[k]/v))


avg_timings = AvgTimings()


class Chronometer:
    def __init__(self):
        self.start()

    def start(self):
        t = timer()
        lap = ('start', 0, t)
        self.laps = [lap]
        self.laps_dict = {'start': lap}

    def lap(self, key):
        t = timer()
        dt = t - self.laps[-1][2]
        lap = (key, dt, t)
        self.laps.append(lap)
        self.laps_dict[key] = lap

    def lap_time(self, key):
        return self.laps_dict[key][1]

    def lap_times(self):
        return [(k, dt) for k, dt, t in self.laps[1:]]

    def total_time(self):
        return self.laps[-1][2] - self.laps[0][2]

def visualize_graph(graph, frame1: str, frame2: str, data, do_show=True):
    if disable_debug:
        return
    print("visualize_graph: ", frame1, frame2)
    lms = graph[frame1]
    pts2D_1 = []
    pts2D_2 = []
    for lm_id in lms:
        obs2 = \
            graph.get_edge_data(str(frame2), str(lm_id))
        if obs2 is not None:
            obs1 = \
                graph.get_edge_data(str(frame1), str(lm_id))
            pts2D_1.append(obs1['feature'])
            pts2D_2.append(obs2['feature'])
    if len(pts2D_1) == 0:
        return
    im1 = data.load_image(frame1)
    im2 = data.load_image(frame2)
    h1, w1, c = im1.shape
    fig, ax = plt.subplots(1)

    obs_d1 = features.\
        denormalized_image_coordinates(np.asarray(pts2D_1), w1, h1)
    obs_d2 = features.\
        denormalized_image_coordinates(np.asarray(pts2D_2), w1, h1)
    print("len(obs_d1): ", len(obs_d1), "len(obs_d2): ", len(obs_d2))
    im = np.hstack((im1, im2))
    ax.imshow(im)
    ax.scatter(obs_d1[:, 0], obs_d1[:, 1], c=[[0, 1, 0]])
    ax.scatter(w1+obs_d2[:, 0], obs_d2[:, 1], c=[[0, 1, 0]])
    ax.set_title(frame1 + "<->" + frame2)

    if do_show:
        plt.show()

def reproject_landmarks(points3D, observations, T_world_to_cam,
                        im, camera, title="", obs_normalized=True, do_show=True):
    """Draw observations and reprojects observations into image"""
    if disable_debug:
        return

    if points3D is None:  # or observations is None:
        return
    if len(points3D) == 0:  # or len(observations) == 0:
        return
    print("T_world_to_cam reproject_landmarks: ", T_world_to_cam)
    pose_world_to_cam = types.Pose()
    pose_world_to_cam.set_rotation_matrix(T_world_to_cam[0:3, 0:3])
    pose_world_to_cam.set_origin(T_world_to_cam[0:3, 3])

    camera_point = pose_world_to_cam.transform_many(points3D)
    points2D = camera.project_many(camera_point)
    fig, ax = plt.subplots(1)
    # im = data.load_image(image)
    # print("Show image ", image)
    if len(im.shape) == 3:
        h1, w1, c = im.shape
    else:
        h1, w1 = im.shape
    pt = features.denormalized_image_coordinates(points2D, w1, h1)
    # print("obs:", obs)
    # print("points2D: ", points2D)
    ax.imshow(im)
    ax.scatter(pt[:, 0], pt[:, 1], c=[[1, 0, 0]])
    if observations is not None:
        if obs_normalized:
            obs = features.denormalized_image_coordinates(observations, w1, h1)
        else:
            obs = observations
        ax.scatter(obs[:, 0], obs[:, 1], c=[[0, 1, 0]])
    ax.set_title(title)
    if do_show:
        plt.show()