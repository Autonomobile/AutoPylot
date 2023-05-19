"""
Analyze the understeer of a vehicle (sim data).
"""

import glob
import json
import os

import matplotlib.pyplot as plt
import numpy as np


def load_json(path):
    """Load json file from path."""
    with open(path, "r") as f:
        return json.load(f)


def analyze(data_path):
    def sort_func(x):
        return float(x.split(os.path.sep)[-1].split(".")[0])

    paths = glob.glob(os.path.join(data_path, "*.json"))
    paths = sorted(paths, key=sort_func)[-250:-50]

    steering = []
    rotation = []

    for path in paths:
        data = load_json(path)
        steering.append(data["steering_angle"] * (180 / np.pi) / 20)
        rotation.append(data["gyro_y"])

    steering = np.array(steering)
    rotation = np.array(rotation)

    # # calculate understeer coefficient
    # understeer = steering / rotation
    # understeer = np.clip(understeer, -1, 1)

    plt.plot(rotation, label="rotation")
    plt.plot(steering, label="steering")
    # plt.plot(understeer, label="understeer")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    current_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_path, "data")
    analyze(data_path)
