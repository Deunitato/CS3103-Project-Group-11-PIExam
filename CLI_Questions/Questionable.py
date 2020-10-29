import csv
import sys
import random



csv.register_dialect('questionDialect',
                     delimiter='|',
                     skipinitialspace=True,
                     quoting=csv.QUOTE_ALL)

def loadQuestions():
    
    mcqQuestions = []
    writtenQuestions = []
    with open('CLI_Questions/QuestionList.csv', 'r') as file:
        reader = csv.reader(file , dialect='questionDialect')
        for row in reader:
            question = row[0].strip()
            questionType = row[1].strip()
            if questionType == "MCQ":
                MCQoptions = row[2].strip().split(',')
                mcqQuestions.append({"question": question , "type": questionType , "values": MCQoptions})
                #MCQquestionID = MCQquestionID + 1
            else:
                writtenQuestions.append({"question": question , "type": questionType})
                #WrittenquestionID = WrittenquestionID + 1
    
    return mcqQuestions, writtenQuestions

def saveAnswers(answerList):
    with open('./data/AnswerList.csv', 'w+') as file:
        titles = ["question", "type", "answer"]
        writer = csv.DictWriter(file, fieldnames = titles, dialect='questionDialect')
        for answer in answerList:
            writer.writerow(answer)


def readMulti():
    content = ""
    while True:
        line = input()
        if line:
            content = content + line + "\r\n"
        else:
            break
    return content

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
    for mcq in mcqDict:
        index = 97
        question = "Q" + str(mcqIndex) + ": " + mcq["question"] + "\n"
        mcqIndex = mcqIndex + 1
        print(question)
        for option in mcq["values"]:
            option = chr(index) + ") " + option + "\n" 
            print(option)
            index = index + 1
        user_answer = input()
        answers.append({"question" :  mcq["question"] , "type" :  mcq["type"], "answer" : user_answer})
    print("\n=================================================\n")
    print("                 Written Questions                 \n")
    print("=================================================\n")
    for written in writtenDict:
        question = "Q" + str(writtenIndex) + ": " + written["question"] + "\n"
        writtenIndex = writtenIndex + 1
        print(question)
        user_answer = readMulti()
        answers.append({"question" :  written["question"] , "type" :  written["type"], "answer" : user_answer})

    return answers


def main():
    MCQs , Writtens = loadQuestions()
    answer = run(MCQs, Writtens)
    #print(answer)
    saveAnswers(answer)


    return "Hello"


if __name__ == "__main__":
    
    main()
