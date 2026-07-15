from app.database import get_connection


def list_documents() -> list[dict]:
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM documents ORDER BY id").fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()
