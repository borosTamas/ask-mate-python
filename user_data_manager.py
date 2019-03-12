import connection


@connection.connection_handler
def insert_new_user(cursor, submission_time, username, h_password):
    cursor.execute("""
    insert into "user" (submission_time, user_name,hashed_password)
    values (%(submission_time)s, %(username)s, %(h_password)s)
    """,
                   {'submission_time': submission_time, 'username': username, 'h_password': h_password})


@connection.connection_handler
def select_all_user(cursor):
    cursor.execute("""
    select * from "user"
    """)
    result=cursor.fetchall()
    return result

