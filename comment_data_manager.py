import connection


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


