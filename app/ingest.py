from app.database import get_connection
from app.fetching import fetch_and_clean


def ingest_document(url: str | None, text: str | None) -> tuple[dict, bool]:
    """Store a single ingested source. Returns (document, created).

    created=False means an existing row for the same url was updated in place.
    """
    if url:
        source_type = "url"
        content = fetch_and_clean(url)
    else:
        source_type = "text"
        content = text

    conn = get_connection()
    try:
        existing = None
        if url:
            existing = conn.execute(
                "SELECT id FROM documents WHERE url = ?", (url,)
            ).fetchone()

        if existing:
            conn.execute(
                "UPDATE documents SET content = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (content, existing["id"]),
            )
            conn.commit()
            row = conn.execute(
                "SELECT * FROM documents WHERE id = ?", (existing["id"],)
            ).fetchone()
            return dict(row), False

        cursor = conn.execute(
            "INSERT INTO documents (url, source_type, content) VALUES (?, ?, ?)",
            (url, source_type, content),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM documents WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
        return dict(row), True
    finally:
        conn.close()
