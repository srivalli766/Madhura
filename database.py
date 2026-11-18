import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = "astrocare.db"


def create_table():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS health_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            heart_rate REAL,
            systolic REAL,
            diastolic REAL,
            temperature REAL,
            glucose REAL,
            glucose_type TEXT,
            hours_since_meal REAL,
            sleep REAL,
            mood TEXT
        )
    """)

    # Add new columns to existing databases if needed
    cursor.execute("PRAGMA table_info(health_records)")
    columns = [column[1] for column in cursor.fetchall()]

    if 'glucose_type' not in columns:
        cursor.execute(
            "ALTER TABLE health_records ADD COLUMN glucose_type TEXT"
        )

    if 'hours_since_meal' not in columns:
        cursor.execute(
            "ALTER TABLE health_records ADD COLUMN hours_since_meal REAL"
        )

    connection.commit()
    connection.close()

def save_health_data(data):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO health_records
        (
            heart_rate, systolic, diastolic,
            temperature, glucose, glucose_type,
            hours_since_meal, sleep, mood
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data['heart_rate'],
        data['systolic'],
        data['diastolic'],
        data['temperature'],
        data['glucose'],
        data['glucose_type'],
        data['hours_since_meal'],
        data['sleep'],
        data['mood']
    ))

    connection.commit()
    connection.close()

def get_health_records():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM health_records ORDER BY id ASC"
    )

    records = cursor.fetchall()

    records = [dict(record) for record in records]

    connection.close()

    return records
def create_astronaut_table():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS astronauts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            agency TEXT NOT NULL,
            mission TEXT NOT NULL,
            role TEXT NOT NULL,
            duration INTEGER,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()
    from werkzeug.security import generate_password_hash


def register_astronaut(data):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    try:
        password_hash = generate_password_hash(data['password'])

        cursor.execute("""
            INSERT INTO astronauts
            (name, agency, mission, role, duration, username, password_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data['name'],
            data['agency'],
            data['mission'],
            data['role'],
            data['duration'],
            data['username'],
            password_hash
        ))

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()
        from werkzeug.security import check_password_hash


def verify_astronaut(username, password):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT password_hash FROM astronauts WHERE username = ?",
        (username,)
    )

    result = cursor.fetchone()
    connection.close()

    if result and check_password_hash(result[0], password):
        return True

    return False