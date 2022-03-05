import base64
import json
import socket
from io import BytesIO

import cv2
import numpy as np
from PIL import Image


def decode_image(str_img):
    tmp_img = np.asarray(Image.open(BytesIO(base64.b64decode(str_img))))
    return cv2.cvtColor(tmp_img, cv2.COLOR_RGB2BGR)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 8080))
s.listen(1)
conn, addr = s.accept()

buffer = ""

while True:
    try:
        data = conn.recv(1024).decode("utf-8")
        if not data:
            break

        buffer += data
        n0 = buffer.find("{")
        n1 = buffer.rfind("}\n")

        if n1 >= 0 and 0 <= n0 < n1:  # there is at lease one message
            msgs = buffer[n0 : n1 + 1].split("\n")
            buffer = buffer[n1:]

            for m in msgs:
                j = json.loads(m)
                # print(j["msg"])
                if isinstance(j["msg"], dict) and "image" in j["msg"].keys():
                    j["msg"]["image"] = decode_image(j["msg"]["image"])
                    cv2.imshow("image", j["msg"]["image"])
                    cv2.waitKey(1)
                else:
                    print(j["msg"])

    except OSError as e:
        # wait for the connection to be established
        conn, addr = s.accept()

    # print(data)
    # conn.sendall(data)

conn.close()
