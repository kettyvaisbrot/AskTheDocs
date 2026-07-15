from app.database import get_connection


def keyword_search(question: str) -> str | None:
    """Very simple SQL LIKE substring search over stored document content.

    Tries each meaningful word from the question until a match is found,
    then returns a short snippet of surrounding context.
    """
    words = [w.strip() for w in question.split() if len(w.strip()) > 2]
    if not words:
        words = [question.strip()]

    conn = get_connection()
    try:
        for word in words:
            row = conn.execute(
                "SELECT content FROM documents WHERE content LIKE ? LIMIT 1",
                (f"%{word}%",),
            ).fetchone()
            if row:
                content = row["content"]
                idx = content.lower().find(word.lower())
                start = max(0, idx - 100)
                end = min(len(content), idx + 200)
                return content[start:end].strip()
        return None
    finally:
        conn.close()
