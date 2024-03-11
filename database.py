import sqlite3 as sq

db = sq.connect('muscle.db')
cursor = db.cursor()


async def db_start() -> None:
    db.execute('PRAGMA foreign_keys = True')
    cursor.execute('CREATE TABLE IF NOT EXISTS muscles ('
                   'id INTEGER PRIMARY KEY, '
                   'name VARCHAR(50),'
                   'image_path TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS users_muscle ('
                   'record_id INTEGER PRIMARY KEY,'
                   'user_id INTEGER,'
                   'muscle_id INTEGER,'
                   'FOREIGN KEY (muscle_id) REFERENCES muscles (id) ON DELETE CASCADE)')
    db.commit()


async def get_random_record():
    cursor.execute("SELECT * FROM muscles ORDER BY RANDOM() LIMIT 1")
    random_record = cursor.fetchone()
    return random_record


async def user_has_seen_all_records(user_id: int) -> bool:
    query = f"SELECT COUNT(DISTINCT muscle_id) = (SELECT COUNT(*) FROM muscles) FROM users_muscle WHERE user_id = {user_id};"
    result = db.execute(query)
    return bool(result.fetchone()[0])


async def insert_record(user_id: int, muscle_id: int) -> None:
    cursor.execute(f'INSERT INTO users_muscle (user_id, muscle_id) VALUES ({user_id}, {muscle_id})')
    db.commit()
    print(f'Запись добавлена ({muscle_id} к {user_id})')


async def is_record_in_db(user_id: int, muscle_id: int) -> bool:
    query = f"SELECT EXISTS(SELECT 1 FROM users_muscle WHERE user_id = {user_id} AND muscle_id = {muscle_id})"
    result = cursor.execute(query)
    return bool(result.fetchone()[0])


def delete_record(user_id: int) -> None:
    sql_delete_query = f"DELETE from users_muscle where user_id = {user_id}"
    cursor.execute(sql_delete_query)
