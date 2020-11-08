from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json

import csv
import sys
import random
import signal
import multiprocessing
import os

csv.register_dialect('questionDialect',
                     delimiter='|',
                     skipinitialspace=True,
                     quoting=csv.QUOTE_ALL)

def loadQuestions():
    mcqQuestions = []
    writtenQuestions = []
    with open('config/QuestionList.csv', 'r') as file:
        reader = csv.reader(file , dialect='questionDialect')
        for row in reader:
            question = row[0].strip()
            questionType = row[1].strip()
            if questionType == "MCQ":
                MCQoptions = row[2].strip().split(',')
                QuestionStruct = {
                                    'type': 'rawlist',
                                    'name': question,
                                    'message': question,
                                    'choices': MCQoptions
                                }
                #mcqQuestions.append({"question": question , "type": questionType , "values": MCQoptions})
                mcqQuestions.append(QuestionStruct)

            else:
                QuestionStruct = {
                            'type': 'editor',
                            'name': question,
                            'message': question,
                            'default': question,
                            'eargs': {
                                'editor':'nano',
                                'ext':'.py'
                            }
                        }
                # writtenQuestions.append({"question": question , "type": questionType})
                writtenQuestions.append(QuestionStruct)

    return mcqQuestions, writtenQuestions

def saveAnswers(answerList):
    if not os.path.exists('data'):
        os.makedirs('data')
    with open('data/AnswerList.csv', 'w+') as file:
        titles = ["question", "type", "answer"]
        writer = csv.DictWriter(file, fieldnames = titles, dialect='questionDialect')
        for answer in answerList:
            writer.writerow(answer)

def run(mcqDict, writtenDict):
    random.shuffle(mcqDict)
    random.shuffle(writtenDict)
    #print(mcqDict)
    mcqIndex = 1
    writtenIndex = 1
    answers = []
    print("\n=================================================\n")
    print("                   MCQ Questions                   \n")
    print("=================================================\n")
    mcqAnswer = prompt(mcqDict)
    for question, answer in mcqAnswer.items():
        answers.append({"question" :  question , "type" :  "MCQ", "answer" : answer})

    print("\n=================================================\n")
    print("                 Written Questions                 \n")
    print("=================================================\n")
    writtenAnswer = prompt(writtenDict)

    for question, answer in writtenAnswer.items():
        answers.append({"question" :  question , "type" : "WRITTEN", "answer" : answer.replace(question + "\n",'')})
    # print("\n")
    # print(mcqAnswer)
    # print("\n")
    #print(writtenAnswer)
    return answers


def main():
    try:
        # Open fd for user input
        sys.stdin = open(0)
        MCQs , Writtens = loadQuestions()
        answer = run(MCQs, Writtens)
        saveAnswers(answer)

    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__": 
    
    p = multiprocessing.Process(target=main, name="Main")
    try:
        p.start()
        p.join(int(sys.argv[1]))

        if p.is_alive():
            p.terminate()
            p.join()

    except KeyboardInterrupt:
        p.terminate()
        p.join()
        sys.exit(0)
