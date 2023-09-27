from .base import connect_db, commit_and_close


def check_user_exists(db_name, username):
    connection, cursor = connect_db(db_name)
    cursor.execute("SELECT * FROM users WHERE username = ?;", (username,))
    user = cursor.fetchone()
    return True if user else False


def add_user(db_name, username):
    connection, cursor = connect_db(db_name)
    cursor.execute("INSERT INTO users(username) VALUES (?);", (username,))
    commit_and_close(connection)
    print('added user:', username)


def add_data(db_name, table_name, **kwargs):
    connection, cursor = connect_db(db_name)

    fields = ', '.join(list(kwargs.keys()))
    values = tuple(kwargs.values())
    sings = ', '.join(['?' for _ in range(len(values))])

    sql = f"INSERT INTO {table_name}({fields}) VALUES ({sings})"

    cursor.execute(sql, values)
    commit_and_close(connection)


def get_user_id(db_name, username):
    connection, cursor = connect_db(db_name)

    sql = "SELECT user_id FROM users WHERE username = ?;"
    cursor.execute(sql, (username,))
    user_id = cursor.fetchone()
    return user_id[0]


def get_user_weather(db_name, user_id):
    connection, cursor = connect_db(db_name)

    sql = "SELECT * FROM weather WHERE user_id = ?;"
    cursor.execute(sql, (user_id,))
    data = cursor.fetchall()
    return data