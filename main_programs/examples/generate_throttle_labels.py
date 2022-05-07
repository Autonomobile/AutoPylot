"""program to generate throttle zones: acceleration zone, braking zone and turn.
"""
import math

import numpy as np
from autopylot.datasets import dataset
from autopylot.utils import io, settings
from tqdm import tqdm

settings = settings.settings


def paths_to_sequences(paths, max_sleep=1):
    """
    Convert a list of paths to a list of sequences.
    """
    sequences = []

    prev_time = None
    for path in tqdm(paths):
        time = dataset.__get_time_stamp(path)
        if prev_time is None:
            sequences.append([path])
            prev_time = time
            continue

        if time - prev_time > max_sleep:
            sequences.append([])

        sequences[-1].append(path)
        prev_time = time

    return sequences


def sliding_average(sequences, window=30):
    """Calculate the average of abs(steering) on a sliding window.

    Args:
        sequences (list[list[float]]): steerings corresponding to the sequences.
        window (int, optional): size of the sliding window. Defaults to 20.

    Returns:
        list[list]: _description_
    """
    seq_averages = []
    for seq in tqdm(sequences):
        averages = []
        for i in range(len(seq)):
            ahead_abs_steering = seq[i : min(i + window, len(seq))]
            if len(ahead_abs_steering) == 0:
                averages.append(0)  # need to find a better default value
            else:
                averages.append(sum(ahead_abs_steering) / len(ahead_abs_steering))

        seq_averages.append(averages)
    return seq_averages


def detect_turns(steering_sequences, turn_th=0.3):
    """
    Args:
        steering_sequences (list[list[float]]): steerings corresponding to the sequences.
        turn_th (float): turn threshold.

    """
    return [np.array(seq) > turn_th for seq in steering_sequences]


def make_labels(path_sequences, turn_sequences, look_ahead=20):
    for (path_seq, turn_seq) in tqdm(zip(path_sequences, turn_sequences)):
        for i in range(len(turn_seq)):
            # look ahead and check if there is a turn
            turns_ahead = turn_seq[i : i + look_ahead]

            distance_before_turn = 0
            while (
                distance_before_turn < len(turns_ahead)
                and not turns_ahead[distance_before_turn]
            ):
                distance_before_turn += 1

            # norm_distance = math.sqrt(distance_before_turn / len(turns_ahead))

            if distance_before_turn == look_ahead:
                label = [1, 0, 0]
            elif distance_before_turn == 0:
                label = [0, 1, 0]
            else:
                label = [0, 0, 1]

            data = io.load_json(path_seq[i])
            data["zone"] = label
            io.save_json(path_seq[i], data)


def main(dataset_path):
    sorted_paths = dataset.sort_paths(dataset.get_every_json_paths(dataset_path))
    path_sequences = paths_to_sequences(sorted_paths)
    raw_steering = [
        [abs(io.load_json(path)["steering"]) for path in seq] for seq in path_sequences
    ]

    steering_sequences = sliding_average(raw_steering)
    turn_sequences = detect_turns(steering_sequences)
    make_labels(path_sequences, turn_sequences)


if __name__ == "__main__":
    main(settings.DATASET_PATH)
