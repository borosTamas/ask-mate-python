import connection

@connection.connection_handler
def login(cursor):
    cursor.execute("""
                    SELECT * 
                    FROM "user"
                    
                    """)

