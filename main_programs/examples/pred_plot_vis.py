import os
from collections import deque

import matplotlib.pyplot as plt
from autopylot.utils import io, settings, vis
from autopylot.models import utils
from matplotlib.animation import FuncAnimation

settings = settings.settings

paths = dataset.sort_paths(dataset.get_every_json_paths(settings.DATASET_PATH))

model1, _ = utils.load_model(
    os.path.normpath("look_ahead_model/look_ahead_model.tflite")
)
model2, _ = utils.load_model(os.path.normpath("synth_model3/synth_model3.tflite"))


fig = plt.figure()
# plt.style.use("classic")
ax1 = fig.add_subplot(1, 1, 1)
ax2 = ax1.twinx()
ax3 = ax2.twinx()
ax4 = ax3.twinx()

###
ax1.clear()
ax1.set_ylim(-1.0, 1.0)
ax1.set_xlim(0, 200)
ax1.set_ylabel("ground_truth", color="blue")

ax2.clear()
ax2.set_ylim(-1.0, 1.0)
ax2.set_xlim(0, 200)
ax2.set_ylabel("pred1", color="red")

ax3.clear()
ax3.set_ylim(-1.0, 1.0)
ax3.set_xlim(0, 200)
ax3.set_ylabel("pred2", color="purple")

ax4.clear()
ax4.set_ylim(-1.0, 1.0)
ax4.set_xlim(0, 200)
ax4.set_ylabel("pred3", color="orange")

(line1,) = ax1.plot([], [], lw=1, color="blue")
(line2,) = ax2.plot([], [], lw=1, color="red")
(line3,) = ax3.plot([], [], lw=1, color="purple")
(line4,) = ax3.plot([], [], lw=1, color="orange")

X = deque([0], maxlen=200)
Y = deque([0], maxlen=200)
Z1 = deque([0], maxlen=200)
Z2 = deque([0], maxlen=200)
Z3 = deque([0], maxlen=200)


def init():
    line1.set_data([], [])
    line2.set_data([], [])
    return line1, line2


def animate(i):
    image_data = io.load_image_data(paths[i])

    pred1 = model1.predict(image_data)
    pred2 = model2.predict(image_data)

    if len(X) < 200:  # fill the X list with numbers from 0 to 200
        X.append(X[-1] + 1)
    Y.append(image_data["steering"])

    # kind of a mess for the moment, will need to refacto
    mean_steer = (
        pred1["steering.0"] + pred1["steering.5"] * 2 + pred1["steering.10"] * 2
    ) / 5
    Z1.append(mean_steer)
    # Z2.append(pred1["steering.5"])
    # Z3.append(pred1["steering.10"])

    image_data["steering"] = mean_steer
    vis_image = vis.vis_all(image_data)
    vis.show(vis_image)

    line1.set_data(X, Y)
    line2.set_data(X, Z1)
    # line3.set_data(X, Z2)
    # line4.set_data(X, Z3)

    return line1, line2, line3, line4


ani = FuncAnimation(
    fig,
    animate,
    init_func=init,
    interval=1,
    frames=len(paths),
)
plt.show()
