import os
from collections import deque

import matplotlib.pyplot as plt
from autopylot.datasets import dataset, preparedata
from autopylot.utils import io, settings, vis
from autopylot.models import utils
from matplotlib.animation import FuncAnimation

settings = settings.settings

paths = dataset.sort_paths(dataset.get_every_json_paths(settings.DATASET_PATH))

model1, model_info1 = utils.load_model(
    os.path.normpath("synth_model1/synth_model1.tflite")
)
model2, model_info2 = utils.load_model(os.path.normpath("renault/renault.tflite"))

prepare_data1 = preparedata.PrepareData(model_info1)
prepare_data2 = preparedata.PrepareData(model_info2)

fig = plt.figure()
# plt.style.use("classic")
ax1 = fig.add_subplot(1, 1, 1)
ax2 = ax1.twinx()
ax3 = ax2.twinx()

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

(line1,) = ax1.plot([], [], lw=1, color="blue")
(line2,) = ax2.plot([], [], lw=1, color="red")
(line3,) = ax3.plot([], [], lw=1, color="purple")

X = deque([0], maxlen=200)
Y = deque([0], maxlen=200)
Z1 = deque([0], maxlen=200)
Z2 = deque([0], maxlen=200)


def init():
    line1.set_data([], [])
    line2.set_data([], [])
    return line1, line2


def animate(i):
    image_data = io.load_image_data(paths[i])
    vis_image = vis.vis_all(image_data)
    vis.show(vis_image)

    input_data1 = prepare_data1(image_data)
    input_data2 = prepare_data2(image_data)

    pred1 = model1.predict(input_data1)
    pred2 = model2.predict(input_data2)

    if len(X) < 200:  # fill the X list with numbers from 0 to 200
        X.append(X[-1] + 1)

    Y.append(image_data["steering"])
    Z1.append(pred1["steering"])
    Z2.append(pred2["steering"])

    line1.set_data(X, Y)
    line2.set_data(X, Z1)
    line3.set_data(X, Z2)

    return line1, line2, line3


ani = FuncAnimation(
    fig,
    animate,
    init_func=init,
    interval=1,
    frames=len(paths),
)
plt.show()
