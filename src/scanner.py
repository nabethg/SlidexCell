"""
SlidexCell - improved data collection of environmental observations in any weather
Copyright © 2023 Nabeth Ghazi

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import cv2
import numpy as np
import traceback

TOTAL_CHLORINE = ("0", "25", "50", "100", "250", "500")
BROMINE = ("0", "0.5/1", "1/2", "3/6.6", "5/11", "10/22")
PH = ("6.2", "6.8", "7.2", "7.6", "7.8", "8.4")
ALKALINITY = ("0", "40", "80", "120", "180", "240")
HARDNESS = ("0", "50", "100", "250", "500", "1000")
FIELDS = (TOTAL_CHLORINE, BROMINE, PH, ALKALINITY, HARDNESS)

C = 4.4  # scaling coefficient

CAM_RES = (1280, 720)


# dimensions of slider
TOTAL_WIDTH = 144.8283
TOTAL_HEIGHT = 150
TOTAL_X = CAM_RES[0] // 2 - (C * TOTAL_WIDTH) // 2
TOTAL_Y = CAM_RES[1] // 2 - (C * TOTAL_HEIGHT) // 2


def draw_square_and_darken(
    img, rect_width=int(C * TOTAL_WIDTH), rect_height=int(C * TOTAL_HEIGHT)
):
    height, width, _ = img.shape

    # mask
    square_mask = np.zeros((height, width), np.uint8)
    center = (width // 2, height // 2)
    half_width = rect_width // 2
    half_height = rect_height // 2
    square_points = [
        (center[0] - half_width, center[1] - half_height),
        (center[0] + half_width, center[1] - half_height),
        (center[0] + half_width, center[1] + half_height),
        (center[0] - half_width, center[1] + half_height),
    ]
    cv2.fillPoly(square_mask, np.array([square_points], np.int32), (255, 255, 255))

    # slider
    img = cv2.rectangle(img, square_points[0], square_points[2], (255, 255, 255), 2)

    # darken mask
    img[np.where(square_mask == 0)] = img[np.where(square_mask == 0)] * 0.5


# dimensions of slider
EDGE = 1.9295
SLIDER_WIDTH = 2 * 6.4656
SLIDER_HEIGHT = TOTAL_HEIGHT - EDGE - 17.7803 - 4.5157
SLIDER_X = (
    5.5683,
    23.6718 + SLIDER_WIDTH / 2,
    48.8874 + 2 * SLIDER_WIDTH / 2,
    64.4047 + 3 * SLIDER_WIDTH / 2,
    85.741 + 4 * SLIDER_WIDTH / 2,
)
SLIDER_Y = 17.7803 + EDGE


def get_outlines():
    res = []
    for x in SLIDER_X:
        x = int(C * x + TOTAL_X)
        y = int(C * SLIDER_Y + TOTAL_Y)
        w = int(C * SLIDER_WIDTH)
        h = int(C * SLIDER_HEIGHT)
        res.append((x, y, w, h))
    return res


OUTLINES = get_outlines()


def draw_outlines(img):
    for outline in OUTLINES:
        x, y, w, h = outline
        pt1 = (x, y)
        pt2 = (x + w, y + h)
        img = cv2.rectangle(img, pt1, pt2, (0, 255, 0), 1)


def get_pointer(contours, outline):
    x_out, y_out, w_out, h_out = outline

    res = None
    max_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            x, y, w, h = cv2.boundingRect(cnt)
            if (x_out <= x and x + w <= x_out + w_out) and (
                y_out <= y and y + h <= y_out + h_out
            ):
                res = cnt
                max_area = area

    return res


def get_value(outline, ptr, field):
    _, y_out, _, h_out = outline
    _, y, _, h = cv2.boundingRect(ptr)
    y += h / 2 - y_out

    cell_h = h_out / len(field)

    return field[int(y) // int(cell_h)]


def display(img):
    draw_square_and_darken(img)
    draw_outlines(img)
    cv2.imshow("Scanner", img)


def cam_scan():
    values = []
    count = 0

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while True:
        try:
            ret, img = cam.read()
            if ret:
                gray = img[:, :, 1]
                _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
                contours, _ = cv2.findContours(
                    thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
                )

                cur_values = []

                for i, outline in enumerate(OUTLINES):
                    ptr = get_pointer(contours, outline)
                    if ptr is None:
                        break
                    img = cv2.drawContours(
                        img,
                        [cv2.approxPolyDP(ptr, 0.01 * cv2.arcLength(ptr, True), True)],
                        -1,
                        (0, 0, 255),
                        2,
                    )
                    cur_values.append(get_value(outline, ptr, FIELDS[i]))

                display(img)
                # print(cur_values)

                if not values and len(cur_values) == len(FIELDS):
                    values = cur_values

                if cur_values and values == cur_values:
                    count += 1

                elif values:
                    count = 0
                    values = cur_values

                if count >= 10:
                    break

                key = cv2.waitKey(1)
                if key == ord("q"):
                    break
        except:
            traceback.print_exc()
            display(img)

            key = cv2.waitKey(1)
            if key == ord("q"):
                break

    # print(values)
    cam.release()
    cv2.destroyAllWindows()
    return values


if __name__ == "__main__":
    print(cam_scan())
