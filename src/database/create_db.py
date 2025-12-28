import sqlite3


def create_master_db():
    conn = sqlite3.connect("passwords")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS master
                 (
                     id
                     INTEGER
                     PRIMARY
                     KEY,
                     password_hash
                     TEXT
                     NOT
                     NULL
                 )''')
    conn.commit()
    conn.close()


def get_master_hash():
    conn = sqlite3.connect("passwords")
    c = conn.cursor()
    c.execute("SELECT password_hash FROM master WHERE id=1")
    result = c.fetchone()
    conn.close()
    return result[0] if result else None


def set_master_hash(password_hash):
    conn = sqlite3.connect("passwords")
    c = conn.cursor()
    c.execute("INSERT INTO master (id, password_hash) VALUES (1, ?)", (password_hash,))
    conn.commit()
    conn.close()


def create_db():
    conn = sqlite3.connect("passwords")
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS passwords
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       login
                       TEXT
                       NOT
                       NULL,
                       password
                       TEXT
                       NOT
                       NULL,
                       description
                       TEXT,
                       updated_at
                       DATETIME
                       NOT
                       NULL
                       DEFAULT
                       CURRENT_TIMESTAMP
                   )
                   """)
    cursor.execute("""
                   CREATE TRIGGER IF NOT EXISTS users_update_time
        AFTER
                   UPDATE ON passwords
                       FOR EACH ROW
                   BEGIN
                   UPDATE passwords
                   SET updated_at = CURRENT_TIMESTAMP
                   WHERE id = OLD.id;
                   END;
                   """)

    conn.commit()
    conn.close()
