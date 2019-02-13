import csv
import os
import time

ANSWERS_HEADER = ['id','submission_time','vote_number','question_id','message','image']
DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
QUESTIONS = DATA_FILE_PATH = os.getenv(
    'DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/question.csv'
ANSWERS = DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/answer.csv'


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
            return result

def collect_answers(id):
    with open(ANSWERS, 'r') as answers:
        result = []
        answers_dict = csv.DictReader(answers, fieldnames=ANSWERS_HEADER)
        for answers in answers_dict:
            if answers['question_id'] == id:
                result.append(answers)
            else:
                result = [{'message':'There is no answers yet.'}]
        return result

def update_question(question_dict):
    with open(QUESTIONS,'r') as old_questions:
        old_question_dict = csv.DictReader(old_questions, fieldnames=DATA_HEADER)
        temporary_list=[]
        for row in old_question_dict:
            if row[id] == question_dict[id]:
                row = question_dict
                temporary_list.append(row)
            else:
                temporary_list.append(row)

    with open(QUESTIONS,'w') as new_qestions:
        new_qestion_dict = csv.DictWriter(new_qestions, fieldnames= DATA_HEADER)
        new_qestion_dict.writeheader()
        for row in temporary_list[1:]:
            new_qestion_dict.writerow(row)


def add_answer(form_data):
    new_id = collect_answers()[-1]['id']
    if new_id == 'id':
        new_id = 1
    else:
        new_id = int(new_id) + 1
    submission_time = int(time.time())
    prepared_data = [item for key, item in form_data.items()]
    prepared_data = list(str(new_id)+str(submission_time)+str(''))+prepared_data
    with open(ANSWERS, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(prepared_data)
