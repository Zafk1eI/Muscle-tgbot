import sqlite3 as sq

db = sq.connect('muscle.db')
cursor = db.cursor()


async def db_start() -> None:
    db.execute('PRAGMA foreign_keys = True')
    cursor.execute('CREATE TABLE IF NOT EXISTS muscles ('
                   'id INTEGER PRIMARY KEY, '
                   'name VARCHAR(50),'
                   'image_path TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS users ('
                   'id_user INTEGER PRIMARY KEY,'
                   'id_muscle INTEGER,'
                   'FOREIGN KEY (id_muscle) REFERENCES muscles (id) ON DELETE CASCADE)')
    db.commit()


async def get_random_record():
    cursor.execute("SELECT * FROM muscles ORDER BY RANDOM() LIMIT 1")
    random_record = cursor.fetchone()
    return random_record


async def insert_record(user_id: int, id_muscle: int) -> None:
    cursor.execute(f'INSERT INTO users (id_user, id_muscle) VALUES ({user_id}, {id_muscle})')
    print(f'Запись добавлена ({id_muscle} к {user_id})')