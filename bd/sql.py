import sqlite3 as sq

# Создание бд
async def db_start():
    global db, cur
    db = sq.connect('sutrudnig.db')
    cur = db.cursor()

    # Определяем существует ли база с таблицей employees, если нет то создаем ее с необходимыми параметрами

    cur.execute('''CREATE TABLE IF NOT EXISTS employees(
        user_id INTEGER PRIMARY KEY,
        name TEXT,
        deportament TEXT,
        point INTEGER,
        last_mission TEXT)
        ''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS mission(
        id_mission INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        data TEXT,
        point INTEGER)
        ''')
    
    db.commit()

# Добавляет вновь прибывших сотрудников
async def create_profile(user_id, username, deportament):
    user = cur.execute("SELECT 1 FROM employees WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    
    if not user:
        cur.execute('INSERT INTO employees VALUES(?, ?, ?, ?, ?)', (user_id, username, deportament, 0, ''))
        db.commit()

# Вытаскиваем все о клиенте
async def sel_emploes(tel_id):
    with sq.connect('sutrudnig.db') as con:
        cur = con.cursor()

        cur.execute(f'SELECT name FROM employees WHERE user_id={tel_id}')
        return cur.fetchall()

# Возвращает количество очков
async def check_point(tel_id):
    with sq.connect('sutrudnig.db') as con:
        cur = con.cursor()

        cur.execute(f'SELECT point FROM employees WHERE user_id={tel_id}')
        return cur.fetchall()
    
# Возвращает рандомную миссию
async def get_random_mission():
    with sq.connect('sutrudnig.db') as con:
        cur = con.cursor()

        cur.execute(f'SELECT * FROM mission ORDER BY RANDOM() LIMIT 1')
        return cur.fetchall()

# Возвращает все об пользователе с ид
async def get_users(tel_id):
    with sq.connect('sutrudnig.db') as con:
        cur = con.cursor()

        cur.execute(f'SELECT name, deportament FROM employees WHERE user_id={tel_id}')
        return cur.fetchall()
    
# Меняем последнию мессию которая выпола персоне
async def set_last_mission(tel_id, last_mission):
    with sq.connect('sutrudnig.db') as con:
        cur = con.cursor()

        cur.execute(f'UPDATE employees SET last_mission={last_mission} WHERE user_id={tel_id}')
        return cur.fetchall()