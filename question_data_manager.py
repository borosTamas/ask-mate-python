import datetime
import connection


@connection.connection_handler
def sort_questions(cursor, option, how):
    option = option
    cursor.execute("""
    SELECT * FROM question
    ORDER BY {option} {how} 
    """.format(option=option,how=how))
    result = cursor.fetchall()
    return result


@connection.connection_handler
def collect_questions(cursor):
    cursor.execute("""
    SELECT * FROM question
    """)
    result = cursor.fetchall()
    return result@connection.connection_handler



@connection.connection_handler
def delete_question(cursor, q_id):
    cursor.execute("""
    delete from question_tag
    where question_id = %(q_id)s;
    delete from comment
    where question_id = %(q_id)s;
    delete from answer
    where question_id = %(q_id)s;  
    delete from question
    where id = %(q_id)s 
    """,
                   {'q_id': q_id})


@connection.connection_handler
def find_searched_questions(cursor, searched_data):
    searched_data = "%" + searched_data + "%"
    cursor.execute("""
    select * from question
    where title  ilike %(searched_data)s
    OR 
    message ilike %(searched_data)s
    """,
                   {'searched_data': searched_data})
    result = cursor.fetchall()
    return result


@connection.connection_handler
def collect_latest_5_question(cursor):
    cursor.execute("""
    SELECT * FROM question
    ORDER BY submission_time DESC 
    LIMIT 5""")
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
def update_question(cursor, datas):
    cursor.execute("""
                    UPDATE question 
                    SET title=%s, message=%s, image=%s
                    WHERE id=%s""",
                   (datas['title'], datas['message'], datas['image'], int(datas['id'])))


@connection.connection_handler
def add_question(cursor, from_data):
    cursor.execute("""
                    INSERT INTO question(submission_time, view_number, vote_number, title, message, image)
                    VALUES (%s,%s,%s, %s,%s,%s)""",
                   (
                       from_data['submission_time'], from_data['view_number'], from_data['vote_number'],
                       from_data['title'],
                       from_data['message'], from_data['image']))


def submission_time_generator():
    submission_time = datetime.datetime.now()
    return submission_time

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

