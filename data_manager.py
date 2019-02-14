import csv
import os
import time
from datetime import datetime

ANSWERS_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']

QUESTIONS_FILE_PATH = os.getenv('QUESTIONS_FILE_PATH', 'sample_data/question.csv')
ANSWERS_FILE_PATH = os.getenv('ANSWERS_FILE_PATH', 'sample_data/answer.csv')


def collect_questions():
    with open(QUESTIONS_FILE_PATH, 'r') as questions:
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
    with open(ANSWERS_FILE_PATH, 'r') as answers:
        result = []
        answers_dict = csv.DictReader(answers, fieldnames=ANSWERS_HEADER)
        for answers in answers_dict:
            if answers['question_id'] == id:
                result.append(answers)
        if len(result) < 1:
            result = [{'message': 'there is no answer yet'}]
        return result


def update_question(question_dict):
    with open(QUESTIONS_FILE_PATH, 'r') as old_questions:
        old_question_dict = csv.DictReader(old_questions, fieldnames=DATA_HEADER)
        temporary_list = []
        for row in old_question_dict:
            if row['id'] == question_dict['id']:
                row = question_dict
                temporary_list.append(row)
            else:
                temporary_list.append(row)

    with open(QUESTIONS_FILE_PATH, 'w') as new_qestions:
        new_qestion_dict = csv.DictWriter(new_qestions, fieldnames=DATA_HEADER)
        new_qestion_dict.writeheader()
        for row in temporary_list[1:]:
            new_qestion_dict.writerow(row)


def collect_all_answer():
    with open(ANSWERS_FILE_PATH, 'r') as all_answer:
        result = []
        all_answer_dict = csv.DictReader(all_answer, fieldnames=ANSWERS_HEADER)
        for answer in all_answer_dict:
            result.append(answer)
        return result


def id_generator():
    new_id = collect_all_answer()[-1]['id']
    if new_id == 'id':
        new_id = 1
    else:
        new_id = int(new_id) + 1
    return new_id


def submission_time_generator():
    submission_time = int(time.time())
    return submission_time


def add_answer(form_data):
    with open(ANSWERS_FILE_PATH, 'a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=ANSWERS_HEADER)
        writer.writerow(form_data)


def new_id(file_name):
    with open(file_name, 'r') as file:
        file_read = csv.DictReader(file, fieldnames=DATA_HEADER)
        for row in file_read:
            new_id = row['id']
        return int(new_id)+1


def csv_questionwriter(csv_file, dictvalue1, dictvalue2):
    with open(csv_file, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER)
        question_id = new_id(csv_file)
        view_counter = 0
        vote_counter = 0
        submission_time = int(time.time())
        writer.writerow({'id': question_id, 'submission_time': submission_time, 'view_number': view_counter,
                         'vote_number': vote_counter, 'title': dictvalue1, 'message': dictvalue2})
