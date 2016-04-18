import cv2


class Object:
    area = None
    aspect_ratio = None
    filled = None
    height = None
    width = None
    shape = None
    center = None


class Image:

    def __init__(self, path):
        self.path = path
        self.image = cv2.imread(path)
        self.gray = cv2.imread(path, 0)
        self.objects = []
        self.conturs = self._get_conturs()
        self._find_objects()

    def _get_conturs(self):
        thresh = self._get_thresh()
        h, contours, _ = cv2.findContours(thresh, 1, 2)
        return contours

    def _get_thresh(self):
        ret, thresh = cv2.threshold(self.gray, 127, 255, 1)
        return thresh

    def _find_objects(self):
        for cnt in self.conturs:
            new_object = Object
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            m = cv2.moments(cnt)
            cx = int(m["m10"] / m["m00"])
            cy = int(m["m01"] / m["m00"])
            color_center = self.image[cx, cy]
            new_object.center = (cx, cy)
            if sum(color_center) > 720:
                new_object.filled = False
            else:
                new_object.filled = True

            new_object.area = cv2.contourArea(cnt)

            _x, _y, _w, _h = cv2.boundingRect(cnt)
            aspect_ratio = float(_w) / _h
            new_object.width = _w
            new_object.height = _h
            new_object.aspect_ratio = aspect_ratio

            if len(approx) == 5:
                new_object.shape = 'pentagon'
                # cv2.drawContours(self.img, [cnt], 0, 255, -1)
            elif len(approx) == 3:
                # print("triangle")
                new_object.shape = 'triangle'
                # cv2.drawContours(self.imgimg, [cnt], 0, (0, 255, 0), -1)
            elif len(approx) == 4:
                # print("square")
                new_object.shape = 'square'
                # cv2.drawContours(self.imgimg, [cnt], 0, (0, 0, 255), -1)
            elif len(approx) == 9:
                # print("half-circle")
                new_object.shape = 'half-circle'
                # cv2.drawContours(self.imgimg, [cnt], 0, (255, 255, 0), -1)
            elif len(approx) > 15:
                # print("circle")
                new_object.shape = 'circle'
                # cv2.drawContours(self.imgimg, [cnt], 0, (0, 255, 255), -1)

            self.objects.append(new_object)
