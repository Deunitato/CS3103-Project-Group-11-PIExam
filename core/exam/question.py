from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json

question = "What is your name?"
question2 = "What is your size?"

questions = [
    {
        'type': 'editor',
        'name': question,
        'message': question,
        'default': question,
        'eargs': {
            'editor':'nano',
            'ext':'.py'
        }
    },
    {
        'type': 'rawlist',
        'name': question2,
        'message': question2,
        'choices': ['XS', 'S', 'M', 'L', 'XL']
    }
]

answers = prompt(questions)
print(answers)