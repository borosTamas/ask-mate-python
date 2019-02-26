import csv
import os
import datetime
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
def find_answer(cursor, a_id):
    cursor.execute("""
    SELECT * from answer
    where id = %(a_id)s
    """,
                   {'a_id': a_id})
    result = cursor.fetchall()
    return result


@connection.connection_handler
def update_answer(cursor, datas):
    cursor.execute("""
                    UPDATE answer
                    SET message=%s, image=%s 
                    WHERE id=%s""",
                   (datas['message'], datas['image'], int(datas['id'])))


@connection.connection_handler
def collect_all_answer(cursor):
    cursor.execute("""
        SELECT * FROM answer
        """)
    result = cursor.fetchall()
    return result


def submission_time_generator():
    submission_time = datetime.datetime.now()
    return submission_time


@connection.connection_handler
def add_answer(cursor, form_data):
    cursor.execute("""
                INSERT INTO answer(submission_time, vote_number, question_id, message, image)
                VALUES (%s, %s, %s, %s, %s)""",
                   (form_data['submission_time'], form_data['vote_number'], form_data['question_id'],
                    form_data['message'], form_data['image']))


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
