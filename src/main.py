import cv2
import numpy as np

import pprint

pp = pprint.PrettyPrinter(indent=4)

images = {}

for x in range(1, 7):
    image_name = '{}.png'.format(x)
    path = '../res/2x1/1/{}'.format(image_name)

    images[image_name] = {}

    img = cv2.imread(path)
    gray = cv2.imread(path, 0)

    ret, thresh = cv2.threshold(gray, 127, 255, 1)

    h, contours,  _ = cv2.findContours(thresh, 1, 2)
    cnt = contours[0]

    approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
    M = cv2.moments(cnt)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    center = img[cX, cY]
    mi = min(center)
    if sum(center) > 720:
        images[image_name]['filled'] = False
    else:
        images[image_name]['filled'] = True

    area = cv2.contourArea(cnt)
    images[image_name]['area'] = area

    _x, _y, _w, _h = cv2.boundingRect(cnt)
    aspect_ratio = float(_w) / _h
    images[image_name]['width'] = _w
    images[image_name]['height'] = _h
    images[image_name]['aspect_ratio'] = aspect_ratio



    # print(len(approx))
    if len(approx) == 5:
        # print("pentagon")
        images[image_name]['shape'] = 'pentagon'
        cv2.drawContours(img, [cnt], 0, 255, -1)
    elif len(approx) == 3:
        # print("triangle")
        images[image_name]['shape'] = 'triangle'
        cv2.drawContours(img, [cnt], 0, (0, 255, 0), -1)
    elif len(approx) == 4:
        # print("square")
        images[image_name]['shape'] = 'square'
        cv2.drawContours(img, [cnt], 0, (0, 0, 255), -1)
    elif len(approx) == 9:
        # print("half-circle")
        images[image_name]['shape'] = 'half-circle'
        cv2.drawContours(img, [cnt], 0, (255, 255, 0), -1)
    elif len(approx) >= 15:
        # print("circle")
        images[image_name]['shape'] = 'circle'
        cv2.drawContours(img, [cnt], 0, (0, 255, 255), -1)

    # cv2.imshow('img', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
pp.pprint(images)


