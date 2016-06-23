import json
from image import Image

problems_config = {
    '2x1': {
        'answers': [str(x) + '.png' for x in range(1, 7)],
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

    def __init__(self, type, number):
        self.type = type
        self.number = number
        self.path = 'res/{}/{}/'.format(self.type, self.number)
        self.config = problems_config[self.type]
        self.answers = []
        self.questions = []

        self._set_answer_images()
        self._set_question_images()

    def get_correct_answer(self):
        with open(self.path + self.config['info']) as info_file:
            info = json.load(info_file)
        return info['answer']

    def _set_answer_images(self):
        for name in self.config['answers']:
            self.answers.append(Image(self.path + name))

    def _set_question_images(self):
        for name in self.config['data']:
            self.questions.append(Image(self.path + name))


# problem = Problem('2x1', '1')
# for answer in problem.answers:
#     print(answer.get_name())
# for question in problem.questions:
#     print(question.get_name())

