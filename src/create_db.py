import sqlite3


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



