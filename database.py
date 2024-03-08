import sqlite3 as sq

db = sq.connect('muscle.db')
cursor = db.cursor()


async def db_start() -> None:
    cursor.execute('CREATE TABLE IF NOT EXISTS muscles ('
                   'id INTEGER PRIMARY KEY, '
                   'name VARCHAR(50),'
                   'image_path TEXT)')
    db.commit()


async def get_random_record():
    cursor.execute("SELECT * FROM muscles ORDER BY RANDOM() LIMIT 1")
    random_record = cursor.fetchone()
    return random_record



