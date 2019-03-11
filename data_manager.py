import os
import datetime
import connection


@connection.connection_handler
def delete_answer(cursor, q_id, a_id):
    cursor.execute("""
    delete from comment
    where question_id = %(q_id)s or answer_id  = %(a_id)s; 
    delete from answer
    where question_id = %(q_id)s and id  = %(a_id)s
    """,
                   {'q_id': q_id, 'a_id': a_id})


@connection.connection_handler
def update_view_number(cursor, q_id):
    cursor.execute("""
    update question
    set view_number = view_number+1
    where id = %(q_id)s
    """,
                   {'q_id': q_id})


@connection.connection_handler
def update_vote_number(cursor, vote, q_id):
    cursor.execute("""
        UPDATE question
        set vote_number = %(vote)s
        WHERE id = %(q_id)s
    """,
                   {'vote': vote, 'q_id': q_id})


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
def add_comment_to_question(cursor, q_id, comment_message):
    cursor.execute("""
                    insert into comment(question_id, message)
                    values (%(q_id)s,%(comment_message)s)
                    
    """,
                   {'q_id': q_id, 'comment_message': comment_message})


@connection.connection_handler
def add_comment_to_answer(cursor, a_id, comment_message):
    cursor.execute("""
                    insert into comment(answer_id, message)
                    values (%(a_id)s,%(comment_message)s)

    """,
                   {'a_id': a_id,  'comment_message': comment_message})


@connection.connection_handler
def collect_comment_to_question(cursor, q_id):
    cursor.execute("""
                    Select message from comment
                    where question_id = %(q_id)s
    """,
                   {'q_id': q_id})
    result = cursor.fetchall()
    return result

@connection.connection_handler
def collect_comment_to_answer(cursor, a_id):
    cursor.execute("""
                    Select message, answer_id from comment
                    where answer_id = %(a_id)s
    """,
                   {'a_id': a_id})
    result = cursor.fetchall()
    return result



