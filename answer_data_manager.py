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


@connection.connection_handler
def add_answer(cursor, form_data):
    cursor.execute("""
                INSERT INTO answer(submission_time, vote_number, question_id, message, image)
                VALUES (%s, %s, %s, %s, %s)""",
                   (form_data['submission_time'], form_data['vote_number'], form_data['question_id'],
                    form_data['message'], form_data['image']))



@connection.connection_handler
def update_vote_number(cursor, vote, q_id):
    cursor.execute("""
        UPDATE question
        set vote_number = %(vote)s
        WHERE id = %(q_id)s
    """,
                   {'vote': vote, 'q_id': q_id})