# Ask the Docs

שירות שאלות-ותשובות על דוקומנטציה טכנית: מקבל מקור (URL או טקסט), שומר אותו, ומאפשר לשאול עליו שאלות בשפה חופשית ולקבל תשובה.

**כתובת חיה:** https://askthedocs-a6fi.onrender.com
**ריפו:** https://github.com/kettyvaisbrot/AskTheDocs

## דוקומנטציה שנבחרה

דוקומנטציית **FastAPI** (fastapi.tiangolo.com) — נבחרה מתוך רשימת ההמלצות של האתגר: אתר בגודל בינוני עם מבנה דפים ברור, ומוכר לי היטב כמפתחת, מה שמקל לבדוק אם התשובות שהמערכת מייצרת נכונות.

## סטאק טכנולוגי

| רכיב | בחירה | סטטוס |
|---|---|---|
| שפה | Python 3.11 | ✅ בשימוש |
| Backend Framework | FastAPI | ✅ בשימוש |
| Database | SQLite (`data/app.db`) | ✅ בשימוש |
| פלטפורמת ענן | Render (Docker Runtime) | ✅ פרוס וחי |
| Vector DB | Qdrant Cloud | מתוכנן לשכבה 2 |
| Embeddings | OpenAI `text-embedding-3-small` | מתוכנן לשכבה 2 |
| LLM | OpenAI `gpt-4o-mini` | מתוכנן לשכבה 1 |
| Frontend | HTML/CSS/JS ואנילי | מתוכנן לשכבה 3 |

## שכבות שהושלמו

- [x] **שכבה 0 (חובה)** — Backend + 3 Endpoints + מסד נתונים אמיתי + דיפלוי חי בענן
- [ ] שכבה 1 (בונוס) — חיבור `/ask` ל-LLM חיצוני
- [ ] שכבה 2 (בונוס) — RAG עם Vector DB (סקרייפינג, Embeddings, Retrieval)
- [ ] שכבה 3 (בונוס) — ממשק צ'אט בדפדפן

## Endpoints ודוגמאות קריאה

### `POST /ingest`

שומר מקור בודד — בדיוק אחד מ-`url` או `text`.

```bash
curl -X POST https://askthedocs-a6fi.onrender.com/ingest \
  -H "Content-Type: application/json" \
  -d '{"url": "https://fastapi.tiangolo.com/tutorial/path-params/"}'
```

תגובה (`201` מסמך חדש / `200` עדכון מסמך קיים עם אותו URL):
```json
{"id": 1, "url": "https://fastapi.tiangolo.com/tutorial/path-params/", "source_type": "url", "created_at": "2026-07-15T19:43:11", "updated_at": "2026-07-15T19:43:11"}
```

### `GET /documents`

מחזיר את כל המסמכים השמורים, כולל תוכן מלא.

```bash
curl https://askthedocs-a6fi.onrender.com/documents
```

### `POST /ask`

**מצב נוכחי (שכבה 0):** חיפוש טקסט פשוט (`SQL LIKE`) על המסמכים השמורים — ללא AI. יורחב בשכבות 1-2 לתשובה מבוססת LLM/RAG.

```bash
curl -X POST https://askthedocs-a6fi.onrender.com/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are path parameters?"}'
```

תגובה:
```json
{"answer": "FastAPI supports path parameters and query parameters out of the box."}
```

## הרצה מקומית

```bash
git clone https://github.com/kettyvaisbrot/AskTheDocs.git
cd AskTheDocs
python -m venv .venv
.venv/Scripts/activate      # Windows; ב-Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # למלא מפתחות API כשנדרשים (שכבות 1-2)
uvicorn app.main:app --reload
```

השרת עולה על `http://127.0.0.1:8000`.

**דיפלוי לענן:** מבוסס `Dockerfile` בשורש הריפו; ב-Render בוחרים Environment: Docker, ומחברים לריפו.

## אימות משתמשים (Auth) בפרודקשן

כרגע אין Auth על ה-Endpoints — נשארו פתוחים לצורך הדגמה, כפי שהותר במפורש בדרישות האתגר. בפרודקשן אמיתי הייתי מוסיפה שכבת אימות (API Key או OAuth2/JWT דרך FastAPI Dependencies) יחד עם הגבלת קצב לכל משתמש/מפתח.

## מה הייתי משפרת עם עוד זמן

- להשלים שכבות 1-3 (LLM חופשי, RAG עם Qdrant, פרונט).
- להוסיף Rate Limiting על `POST /ask` — הושמט בכוונה בשלב הנוכחי עקב אילוץ זמן (מתועד כסיכון פתוח בתוכנית ההנדסית).
- להוסיף בדיקת עשן אוטומטית ל-`/ask`.
- לבדוק את התנהגות הדיסק של SQLite ב-Render Free Tier מול Redeploy, ולשקול Persistent Disk אם נדרשת עמידות נתונים מלאה בפרודקשן.

---
*מסמך זה מתעדכן עם השלמת כל שכבה נוספת.*
