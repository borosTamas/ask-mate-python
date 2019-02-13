import csv
import os

ANSWERS_HEADER = ['id','submission_time','vote_number','question_id','message,image']
DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
QUESTIONS = DATA_FILE_PATH = os.getenv(
    'DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else '/home/levente/Desktop/web/ask mate/ask-mate-python/sample_data/question.csv'
ANSWERS = DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else '/home/levente/Desktop/web/ask mate/ask-mate-python/sample_data/answer.csv'


def collect_questions():
    with open(QUESTIONS, 'r') as questions:
        result = []
        questions_dict = csv.DictReader(questions, fieldnames=DATA_HEADER)
        for question in questions_dict:
            result.append(question)
        return result

def find_question(id):
    list_of_questions = collect_questions()
    for question in list_of_questions:
        if question['id'] == id:
            result = question
            print(result["title"])
            return result

def collect_answers():
    with open(ANSWERS, 'r') as answers:
        result = []
        answers_dict = csv.DictReader(answers, fieldnames=ANSWERS_HEADER)
        for answers in answers_dict:
            result.append(answers)
        return result
