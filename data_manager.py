import csv
import os
import time
import connection

ANSWERS_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']

QUESTIONS_FILE_PATH = os.getenv('QUESTIONS_FILE_PATH', 'sample_data/question.csv')
ANSWERS_FILE_PATH = os.getenv('ANSWERS_FILE_PATH', 'sample_data/answer.csv')


@connection.connection_handler
def collect_questions(cursor):
    cursor.execute("""
    SELECT * FROM question
    """)
    result = cursor.fetchall()
    return result


@connection.connection_handler
def find_question(cursor, q_id):
    cursor.execute("""
    SELECT * from question
    where id = %(q_id)s
    """,
                   {'q_id': q_id})
    result = cursor.fetchall()
    return result


@connection.connection_handler
def update_view_number(cursor, q_id):
    cursor.execute("""
    update question
    set view_number = view_number+1
    where id = %(q_id)s
    """,
                   {'q_id': q_id})


def update_vote_number(question, vote):
    vote_number = question['vote_number']
    if vote == 'up':
        vote_number = int(vote_number) + 1
    elif vote == 'down':
        vote_number = int(vote_number) - 1
    question['view_number'] = vote_number
    update_question(question)


@connection.connection_handler
def collect_answers(cursor, q_id):
    cursor.execute("""
    SELECT * from answer
    where question_id = %(q_id)s
    """,
                   {'q_id': q_id})

    result = cursor.fetchall()
    return result


@connection.connection_handler
def update_question(cursor, datas):
    cursor.execute("""
                    UPDATE question 
                    SET message=%s, image=%s
                    WHERE id=%s""",
                   (datas['message'], datas['image'], int(datas['id'])))


@connection.connection_handler
def update_answer(cursor, datas):
    cursor.execute("""
                    UPDATE answer
                    SET message=%s, image=%s 
                    WHERE id=%s""",
                   (datas['message'], datas['image'], int(datas['id'])))


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


@connection.connection_handler
def add_answer(cursor, form_data):
    cursor.execute("""
                INSERT INTO answer(submission_time, vote_number, question_id, message, image)
                VALUES (%s, %s, %s, %s, %s, %s)""",
                   (form_data['submission_time'], form_data['vote_number'], form_data['question_id'],
                    form_data['message'], form_data['image']))


def new_id(file_name):
    with open(file_name, 'r') as file:
        file_read = csv.DictReader(file, fieldnames=DATA_HEADER)
        for row in file_read:
            new_id = row['id']
        return int(new_id) + 1


def csv_questionwriter(csv_file, dictvalue1, dictvalue2):
    with open(csv_file, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER)
        question_id = new_id(csv_file)
        view_counter = 0
        vote_counter = 0
        submission_time = int(time.time())
        writer.writerow({'id': question_id, 'submission_time': submission_time, 'view_number': view_counter,

                         'vote_number': vote_counter, 'title': dictvalue1, 'message': dictvalue2})


@connection.connection_handler
def add_question(cursor, message):
    submission_time = "time"
    # int(time.time())
    vote_number = "vote_number"
    image = "img"
    view_number = "view_number"
    title = "title"
    cursor.execute("""
                    INSERT INTO question(submission_time, view_number, vote_number, title, message, image)
                    VALUES (%(submission_time)s,%(view_number)s,%(vote_number)s, %(title)s,%(message)s,%(image)s);
                   """,

                   {'submission_time': submission_time, 'view_number': view_number, 'vote_number': vote_number,
                    'title': title, 'message': message, 'image': image})
