import connection

@connection.connection_handler
def insert_new_user(cursor, submission_time, username, h_password, user_reputation):
    cursor.execute("""
    insert into "user" (submission_time, user_name,hashed_password, reputation)
    values (%(submission_time)s, %(username)s, %(h_password)s, %(user_reputation)s)
    """,
    {'submission_time':submission_time,'username': username, 'h_password': h_password, 'user_reputation':user_reputation})



@connection.connection_handler
def get_user_id(cursor, username):
    cursor.execute("""
    select id from "user"
    where user_name = %(username)s
    """,
                   {'username': username})
    result = cursor.fetchone()
    return result
