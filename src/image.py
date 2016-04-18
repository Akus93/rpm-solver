import cv2
import operator


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
        self._remove_duplicates()

    def _get_conturs(self):
        thresh = self._get_thresh()
        h, contours, _ = cv2.findContours(thresh, 1, 2)
        return contours

    def _remove_duplicates(self):
        without_duplicates = []
        for x in self.objects:
            if without_duplicates:
                duplicat = False
                for y in without_duplicates:
                    if y.center == x.center or \
                            y.center == tuple(map(operator.add, x.center, (1, 0))) or \
                            y.center == tuple(map(operator.add, x.center, (0, 1))) or \
                            y.center == tuple(map(operator.sub, x.center, (1, 0))) or \
                            y.center == tuple(map(operator.sub, x.center, (0, 1))):
                        duplicat = True
                if not duplicat:
                    without_duplicates.append(x)
            else:
                without_duplicates.append(x)
        self.objects = without_duplicates

    def _get_thresh(self):
        ret, thresh = cv2.threshold(self.gray, 127, 255, 1)
        return thresh

    def _find_objects(self):
        for cnt in self.conturs:
            new_object = Object()
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
            elif len(approx) == 3:
                new_object.shape = 'triangle'
            elif len(approx) == 4:
                new_object.shape = 'square'
            elif len(approx) == 9:
                new_object.shape = 'half-circle'
            elif len(approx) >= 15:
                new_object.shape = 'circle'

            self.objects.append(new_object)
