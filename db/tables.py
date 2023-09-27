from db.base import connect_db, commit_and_close


def create_users_table():
    connection, cursor = connect_db("../weather.db")
    sql = """
        DROP TABLE IF EXISTS users;
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT
        );
    """
    cursor.executescript(sql)

    commit_and_close(connection)

    create_users_table()


def create_weather_table():
    connection, cursor = connect_db("../weather.db")

    sql = """
        DROP TABLE IF EXISTS weather;
        CREATE TABLE IF NOT EXISTS weather(
            weather_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            tz INTEGER,
            dt DATETIME,
            sunrise DATETIME,
            sunset DATETIME,
            description TEXT,
            temp DECIMAL,
            speed DECIMAL,
            
            user_id INTEGER REFERENCES users(user_id)
        );
    """

    cursor.executescript(sql)
    commit_and_close(connection)

    create_weather_table()

