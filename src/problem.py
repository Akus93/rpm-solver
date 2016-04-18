import json
from image import Image

problems_config = {
    '2x1': {
        'answers': [str(x) + '.png' for x in range(1, 8)],
        'data': ['a.png', 'b.png', 'c.png'],
        'full': 'full.png',
        'info': 'info.json',
    },
    '2x2': {

    },
    '3x3': {

    }
}


class Problem:

    def __init__(self, _type, _number):
        self.type = _type
        self.number = _number
        self.path = '../res/{}/{}/'.format(self.type, self.number)
        self.config = problems_config[self.type]
        self.correct_answer = self.get_correct_answer()
        self.answer_images = []
        self.data_images = []

        self._get_answer_images()
        self._get_data_images()

    def get_correct_answer(self):
        info = None
        with open(self.path + self.config['info']) as info_file:
            info = json.load(info_file)
        return info['answer']

    def _get_answer_images(self):
        for name in self.config['answers']:
            self.answer_images.append(Image(self.path + name))

    def _get_data_images(self):
        for name in self.config['data']:
            self.data_images.append(Image(self.path + name))


problem = Problem('2x1', '1')
for x in problem.answer_images:
    print(x)
    for y in x.objects:
        print(y.center)

