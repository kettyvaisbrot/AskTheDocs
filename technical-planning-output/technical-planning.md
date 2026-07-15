<div dir="rtl" lang="he">

# תוכנית הנדסית — "Ask the Docs"

מסמך מקור: `Final_Challenge_LiveCoding_RAG_Backend_260713_084032.pdf`
תשומה: `requirements-analysis-output/requirements-analysis.md`

מסמך זה הוא ה-Blueprint ההנדסי המלא למימוש. הוא מבוסס במלואו על ניתוח הדרישות שבוצע קודם לכן, ועל סדרת החלטות טכניות שאושרו במפורש על ידי המפתח/ת בסשן תכנון אינטראקטיבי. כל החלטה שלא הוגדרה במפורש במסמך הדרישות — נשאלה, ולא הומצאה.

---

## 1. Executive Goal

לבנות ולפרוס בענן, בתוך חלון זמן של 90 דקות, את מערכת "Ask the Docs" — שירות שאלות-ותשובות מבוסס RAG על דוקומנטציית FastAPI — תוך מימוש **כל ארבע השכבות** (0 חובה, 1-3 בונוס), בסטאק: FastAPI + SQLite + Qdrant + OpenAI, עם דיפלוי חי ל-Render.

## 2. Business Objective

לאפשר שאילתת שאלות חופשיות על דוקומנטציה טכנית אמיתית ולקבל תשובות מדויקות, מעוגנות במקור, עם ציטוט, תוך הימנעות מהמצאת מידע (Hallucination). כאשר השאלה חורגת מתחום הידע שנאסף — להשיב במפורש "אין לי מידע על זה". (מקור: ניתוח הדרישות, סעיפים 2-3).

## 3. Planning Scope

### In Scope
- שכבה 0 (חובה): Backend, 3 Endpoints, DB אמיתי, דיפלוי חי.
- שכבה 1 (בונוס): חיבור `/ask` ל-LLM חיצוני (OpenAI).
- שכבה 2 (בונוס): צנרת אינדוקס (סקרייפינג רשימת URL קבועה, Chunking, Embeddings, Qdrant) + Retrieval ב-`/ask`.
- שכבה 3 (בונוס): ממשק צ'אט סטטי (HTML/CSS/JS) מוגש על ידי אותו שרת Backend.
- בדיקת עשן אחת ל-`POST /ask` (אם נותר זמן).
- תיעוד README כולל סעיף Auth-בפרודקשן, כנדרש במסמך המקור.

### Out of Scope
- אימות משתמשים (Auth) על ה-Endpoints — הוחרג במפורש במסמך המקור.
- Rate Limiting על `POST /ask` — הוחלט להשמיט עקב אילוץ זמן (החלטת מפתח/ת; מתועד כסיכון פתוח בסעיף 17-18).
- צינור CI/CD — דיפלוי אוטומטי/ידני דרך Render על push ל-Git בלבד.
- Logging/Monitoring מעבר לרישום הסטנדרטי של ה-Framework/הפלטפורמה.
- Crawling אוטומטי רב-דפי — הוחלף ברשימת URL קבועה מראש שנבחרת ידנית.
- תמיכה במספר אתרי דוקומנטציה בו-זמנית / ריבוי-דיירים (Multi-tenant).

### Mandatory
שכבה 0 בלבד — לפי כלל "שכבה 0 היא חובה" (מקור: ניתוח הדרישות, סעיף 8).

### Optional
שכבות 1, 2, 3 — כל שכבה נספרת רק אם השכבה שמתחתיה עובדת בפועל (Layer Gating, מקור: ניתוח הדרישות, סעיף 22).

---

## 4. Engineering Decisions

| # | החלטה | אפשרות שנבחרה | סיבה | מקור |
|---|---|---|---|---|
| D1 | היקף תכנון | תכנון מלא לכל 4 השכבות | הציפייה למקסם שכבות; הפירוק לצעדים קטנים ייעשה בנפרד לאחר מכן | Developer Decision |
| D2 | Backend Framework | FastAPI (Python) | מוכר, מהיר לפריסה, אקוסיסטם Python חזק ל-RAG/Embeddings | Developer Decision |
| D3 | Database (מטא-דאטה) | SQLite על דיסק | הכי מהיר להקמה מקומית, עומד בדרישת "שורד ריסטארט" באופן עקרוני | Developer Decision |
| D4 | אתר דוקומנטציה | דוקומנטציית FastAPI | נבחר מתוך רשימת ההמלצות במסמך המקור | Developer Decision (מתוך רשימת המסמך) |
| D5 | ספק LLM | OpenAI (GPT) | מוכר למפתח/ת, ממזער זמן אינטגרציה | Developer Decision |
| D6 | מודל LLM ספציפי | gpt-4o-mini | מהיר וזול, מתאים לחלון 90 דקות | Developer Decision |
| D7 | Vector DB | Qdrant (מנוהל, Qdrant Cloud) | Free Tier עננ י, ללא צורך בהתקנה מקומית | Developer Decision |
| D8 | ספק Embeddings | OpenAI text-embedding-3-small (1536 ממדים) | זול ומהיר, מספיק לדוקומנטציה טכנית | Developer Decision |
| D9 | פלטפורמת ענן | Render | קלה לדיפלוי מ-Git, שכבת חינם מספיקה | Developer Decision |
| D10 | אירוח פרונט | על אותו שרת Backend (Static מוגש על ידי FastAPI) | פשוט יותר, אין צורך ב-CORS/דיפלוי נפרד תחת אילוץ זמן | Developer Decision |
| D11 | טכנולוגיית פרונט | HTML/CSS/JS ואנילי | הכי מהיר למימוש ולדיפלוי בזמן קצר | Developer Decision |
| D12 | אלגוריתם חיפוש שכבה 0 | SQL LIKE / התאמת תת-מחרוזת פשוטה | תואם דרישת "חיפוש טקסט פשוט, בלי AI" | Developer Decision (בהתאם לדרישת המסמך) |
| D13 | התנהגות POST /ingest (שכבה 0) | שומר רק את הדף/הטקסט הבודד שנשלח, ללא Crawl | תואם את חוזה שכבה 0; Crawl רב-דפי מבוצע רק בשכבה 2 בנפרד | Developer Decision |
| D14 | תוכן שנשמר ב-ingest | URL (אופציונלי) או טקסט (אופציונלי) + תוכן מלא לאחר ניקוי | תואם "מקבל מקור (URL או טקסט) ושומר אותו" | Requirement Document |
| D15 | ייחודיות URL | `url` הוא UNIQUE כאשר קיים; ingest חוזר על אותו URL מעדכן את הרשומה הקיימת | מניעת כפילויות בסקריפט האינדוקס שקורא ל-/ingest שוב ושוב | Developer Decision |
| D16 | הבחנה בין סוגי קלט | שדה `source_type` ('url' / 'text') | נדרש כדי להבחין בין ingest מבוסס-URL לבין טקסט גולמי, בפרט לצורך שכבת האינדוקס | Developer Decision |
| D17 | תוכן GET /documents | רשימת מסמכים כוללת את התוכן המלא של כל מסמך | הוחלט במפורש; ללא Pagination | Developer Decision |
| D18 | מנגנון אינדוקס שכבה 2 | סקריפט CLI עצמאי חד-פעמי (`scripts/index_docs.py`) הקורא ל-`/ingest` על רשימת ~15-20 URL קבועה מראש, ואז מבצע Chunking+Embeddings+Qdrant upsert | הפרדה ברורה בין ingest כללי (משותף לכל המערכת) לבין תהליך האינדוקס הספציפי לשכבה 2; אינדוקס אינו מופעל אוטומטית מכל ingest | Developer Decision |
| D19 | היקף גריפה לשכבה 2 | ~15-20 דפים נבחרים ידנית מדוקומנטציית FastAPI | תואם המלצת המסמך "עדיף עשרים דפים שעובדים מצוין" | Requirement Document |
| D20 | אסטרטגיית Chunking | פיצול היררכי: לפי כותרות HTML (h1/h2/h3) ← פסקאות ← משפטים, עד ≤500 טוקנים לצ'אנק | תואם אזהרת המסמך מפני "צ'אנקים ענקיים"; היררכיה סמנטית מפורטת נקבעה על ידי המפתח/ת | Developer Decision |
| D21 | Retrieval — כמות צ'אנקים | top-k = 4 | איזון בין דיוק להיקף Context | Developer Decision |
| D22 | סף "אין לי מידע" | cosine similarity < 0.75 עבור כל 4 התוצאות | תואם דרישת "שאלה מחוץ לתחום מקבלת 'אין לי מידע על זה'" | Requirement Document (הדרישה) + Developer Decision (הערך המספרי) |
| D23 | פורמט ציטוט מקור | רשימת URL ייחודיים (Deduplicated) של המסמכים שמהם נשלפו הצ'אנקים | תואם "עם ציון הדף שממנו נשלפה" | Requirement Document (הדרישה) + Developer Decision (הפורמט) |
| D24 | טיפול בשגיאות | קודי HTTP סטנדרטיים (400/404/422/500) עם גוף `{"error": "..."}` | פשוט, תואם קריטריון ההערכה "טיפול בסיסי בשגיאות" | Developer Decision |
| D25 | Rate Limiting | לא ממומש (Out of Scope) | הוחלט להשמיט עקב אילוץ זמן; מתועד כסיכון פתוח | Developer Decision |
| D26 | Auth | לא ממומש; מתועד ב-README כיצד היה נוסף בפרודקשן | דרישה מפורשת | Requirement Document |
| D27 | Logging/Monitoring | רישום סטנדרטי של ה-Framework/הענן בלבד | מחוץ להיקף 90 הדקות | Developer Decision |
| D28 | CI/CD | ללא Pipeline; דיפלוי אוטומטי/ידני דרך Render על push ל-Git | מחוץ להיקף 90 הדקות | Developer Decision |
| D29 | בדיקות (Testing) | בדיקת עשן אחת ל-`POST /ask`, כצעד אחרון בתוכנית העבודה | אופציונלי לפי המסמך, אך נכלל לפי בקשת המפתח/ת | Developer Decision |
| D30 | סודות | כל המפתחות (`OPENAI_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`) ב-Environment Variables, לא בקוד/Git | דרישה מפורשת | Requirement Document |
| D31 | שיטת פריסה ב-Render | Docker Runtime עם `Dockerfile` (לא Native Python Runtime) | שליטה מלאה וריפרודוקביליות של סביבת ההרצה; הוחלט בשלב הדיפלוי לאחר שהוחמץ בסבב השאלות המקורי ותוקן | Developer Decision (retroactive — נשאלה ואושרה בשלב הביצוע, M0.6) |

---

## 5. Technology Stack

| שכבה טכנולוגית | בחירה | הערה |
|---|---|---|
| שפת תכנות | Python 3.11+ | תואם FastAPI |
| Backend Framework | FastAPI | D2 |
| שרת ASGI | Uvicorn | סטנדרטי ל-FastAPI |
| Database (מטא-דאטה) | SQLite (קובץ על דיסק) | D3 |
| Vector DB | Qdrant Cloud (מנוהל) | D7 |
| Embeddings Provider | OpenAI `text-embedding-3-small` | D8 |
| LLM Provider | OpenAI `gpt-4o-mini` | D5, D6 |
| Frontend | HTML/CSS/JS ואנילי, מוגש כ-Static על ידי FastAPI | D10, D11 |
| Cloud Hosting | Render (Web Service, Free Tier) | D9 |
| ניהול סודות | Render Environment Variables | D30 |

---

## 6. High-Level Architecture

```
                         User
                          │
                          ▼
                 ┌─────────────────┐
                 │   Front / UI    │  Static HTML/CSS/JS  (שכבה 3)
                 │  (served by FastAPI)                   │
                 └────────┬────────┘
                          │ HTTP (same origin — no CORS)
                          ▼
                 ┌─────────────────┐
                 │  FastAPI Backend│  Uvicorn                (שכבה 0)
                 │  POST /ingest   │
                 │  GET  /documents│
                 │  POST /ask      │
                 └───┬─────────┬───┘
                     │         │
          ┌──────────▼──┐   ┌──▼──────────────┐
          │   SQLite    │   │  OpenAI GPT API │  gpt-4o-mini    (שכבה 1)
          │ documents   │   │  (LLM)          │
          └─────────────┘   └────────▲────────┘
                                      │ Context (top-4 chunks)
                             ┌────────┴────────┐
                             │   Qdrant Cloud  │  Embeddings + Retrieval (שכבה 2)
                             │ (Vector DB)     │  1536-dim, cosine
                             └────────▲────────┘
                                      │ upsert (Index)
                             ┌────────┴────────┐
                             │ scripts/        │  CLI חד-פעמי:
                             │ index_docs.py   │  scrape → clean → chunk →
                             │ (ETL)           │  embed (OpenAI) → upsert (Qdrant)
                             └─────────────────┘
                                      │
                                      ▼
                         ~15-20 URL קבועים מראש
                         מדוקומנטציית FastAPI
```

הערה: `scripts/index_docs.py` קורא בעצמו ל-`POST /ingest` עבור כל URL ברשימה (כדי לשמור גם ב-SQLite), ולאחר מכן מבצע Chunking + Embeddings + Qdrant upsert (D18).

---

## 7. Database Design

### 7.1 SQLite — טבלת `documents`

| שדה | טיפוס | Required/Nullable | ברירת מחדל | PK/FK | אילוצים |
|---|---|---|---|---|---|
| `id` | INTEGER | Required | — | PRIMARY KEY, AUTOINCREMENT | — |
| `url` | TEXT | Nullable | NULL | — | UNIQUE (מתעלם מ-NULL מרובים, לפי סמנטיקת UNIQUE של SQLite) |
| `source_type` | TEXT | Required | — | — | CHECK (`source_type` IN ('url','text')) |
| `content` | TEXT | Required | — | — | — |
| `created_at` | TIMESTAMP | Required | `CURRENT_TIMESTAMP` | — | — |
| `updated_at` | TIMESTAMP | Required | `CURRENT_TIMESTAMP` | — | מתעדכן בכל re-ingest של אותו URL |

אינדקסים: `UNIQUE INDEX` על `url` (חלקי, כאשר לא NULL).

מקור: החלטות D14–D17, ואישור מפורש של המפתח/ת על הסכמה הסופית.

### 7.2 Qdrant — Collection `fastapi_docs_chunks`

| הגדרה | ערך |
|---|---|
| Vector size | 1536 |
| Distance metric | Cosine |
| Payload fields | `document_id` (int, מקשר ל-SQLite `documents.id`), `url` (string, לצורך ציטוט מהיר ללא JOIN), `chunk_text` (string), `chunk_index` (int, סדר בתוך המסמך) |

מקור: החלטה D7, D8, D20, D23, ואישור מפורש של המפתח/ת.

**הערה חשובה (לא הוזכרה במפורש במסמך המקור — Developer Attention Required):** ל-Chunk/Embedding אין ייצוג בטבלה יחסית ב-SQLite; המידע היחיד עליהם חי ב-Qdrant. אם יידרש בעתיד Debug/שאילתות SQL על תוכן הצ'אנקים — יהיה צורך בהחלטה נפרדת (לא בהיקף התוכנית הנוכחית).

---

## 8. API Contracts

### 8.1 `POST /ingest`

**בקשה** — בדיוק אחד מהשדות הבאים חייב להימסר (הדדית בלעדיים):
```json
{ "url": "https://fastapi.tiangolo.com/tutorial/first-steps/" }
```
או
```json
{ "text": "טקסט גולמי חופשי..." }
```

**תגובה — הצלחה (מסמך חדש):** `201 Created`
```json
{
  "id": 1,
  "url": "https://fastapi.tiangolo.com/tutorial/first-steps/",
  "source_type": "url",
  "created_at": "2026-07-15T10:00:00Z",
  "updated_at": "2026-07-15T10:00:00Z"
}
```

**תגובה — הצלחה (עדכון URL קיים):** `200 OK` (אותו מבנה גוף, `updated_at` מרוענן)

**שגיאות:**
- `422 Unprocessable Entity` — אם לא נמסר אף שדה, או נמסרו שני השדות יחד: `{"error": "exactly one of url or text is required"}`
- `500 Internal Server Error` — כשל בשליפת ה-URL (בשכבה 0: כשל HTTP; אין Retry logic בהיקף התוכנית)

### 8.2 `GET /documents`

**תגובה:** `200 OK`
```json
[
  {
    "id": 1,
    "url": "https://fastapi.tiangolo.com/tutorial/first-steps/",
    "source_type": "url",
    "content": "<תוכן מלא של המסמך>",
    "created_at": "2026-07-15T10:00:00Z",
    "updated_at": "2026-07-15T10:00:00Z"
  }
]
```
ללא Pagination (D17). רשימה ריקה `[]` אם אין מסמכים.

### 8.3 `POST /ask`

חוזה ה-Endpoint **מתפתח** לאורך השכבות (כל שכבה מחליפה/מרחיבה את מימוש הקודמת; החוזה הסופי המוגש הוא זה של שכבה 2):

| שכבה | לוגיקה פנימית | תגובה |
|---|---|---|
| 0 | SQL LIKE על `documents.content` | `{"answer": "<קטע טקסט תואם>"}` |
| 1 | קריאה ל-`gpt-4o-mini` ללא Context | `{"answer": "<תשובה חופשית מהמודל>"}` |
| 2 (סופי) | Retrieval מ-Qdrant (top-4, סף 0.75) → הזרקת Context ל-`gpt-4o-mini` | ראה מטה |

**בקשה (כל השכבות):**
```json
{ "question": "How do I define a path parameter in FastAPI?" }
```

**תגובה — שכבה 2 (סופית), מידע נמצא:** `200 OK`
```json
{
  "answer": "כדי להגדיר Path Parameter ב-FastAPI...",
  "sources": [
    "https://fastapi.tiangolo.com/tutorial/path-params/"
  ]
}
```

**תגובה — שכבה 2 (סופית), אין מידע רלוונטי (כל top-4 מתחת לסף 0.75):** `200 OK`
```json
{ "answer": "אין לי מידע על זה", "sources": [] }
```

**שגיאות:**
- `422 Unprocessable Entity` — שאלה חסרה/ריקה: `{"error": "question is required"}`
- `500 Internal Server Error` — כשל בקריאה ל-OpenAI או ל-Qdrant

### 8.4 קבצים סטטיים (שכבה 3)

`GET /` (וכל נתיב static רלוונטי) — מגיש את דף הצ'אט (`index.html` + CSS/JS), הקורא בצד לקוח ל-`POST /ask` באמצעות `fetch`.

---

## 9. External Integrations

| אינטגרציה | תפקיד | פרטי חיבור |
|---|---|---|
| OpenAI API — Embeddings | יצירת וקטורים לצ'אנקים (שכבה 2) ולשאלות נכנסות | `OPENAI_API_KEY` ב-Env Var; מודל `text-embedding-3-small` |
| OpenAI API — Chat Completions | ניסוח תשובות (שכבות 1-2) | אותו `OPENAI_API_KEY`; מודל `gpt-4o-mini` |
| Qdrant Cloud | אחסון ואחזור Embeddings (שכבה 2) | `QDRANT_URL`, `QDRANT_API_KEY` ב-Env Vars |
| דוקומנטציית FastAPI (fastapi.tiangolo.com) | מקור הנתונים לגריפה (שכבה 2) | רשימת ~15-20 URL קבועה מראש, ללא אימות נדרש (אתר ציבורי) |
| Render | אחסון ודיפלוי ה-Backend | Git-based deploy |

---

## 10. Infrastructure

- **שרת יישום:** Render Web Service (Free Tier), Python 3.11, `uvicorn` כ-ASGI server.
- **אחסון קבצים (SQLite):** קובץ מקומי על דיסק השירות (`data/app.db`).
  **סיכון פתוח (Developer Attention Required):** ב-Render, Free Tier אינו כולל Persistent Disk מובטח — ייתכן שהדיסק מתאפס בעת Redeploy חדש (בניגוד ל-Restart רגיל). יש לוודא זאת בפועל בזמן ההקמה; ראו סעיף 17 (סיכונים).
- **אחסון Vector:** Qdrant Cloud, Cluster בשכבת חינם, נפרד מהשרת עצמו.
- **משתני סביבה נדרשים (Render Dashboard, לא ב-Git):**
  - `OPENAI_API_KEY`
  - `QDRANT_URL`
  - `QDRANT_API_KEY`

---

## 11. Deployment Strategy

1. ריפו Git ציבורי, עם `.gitignore` הכולל `.env`, `*.db` (אם רלוונטי בזמן פיתוח מקומי), `__pycache__/`.
2. **פריסה ב-Render באמצעות Docker Runtime (D31):** קובץ `Dockerfile` בשורש הריפו (Python 3.11-slim, מתקין `requirements.txt`, מריץ `uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}`). ב-Render בוחרים **Environment: Docker** — Render מזהה את ה-`Dockerfile` אוטומטית ובונה ממנו; אין צורך למלא Build/Start Command בממשק (הם מוגדרים בתוך הקובץ עצמו).
3. הגדרת משתני הסביבה (`OPENAI_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`) ישירות בממשק Render — לא בקוד.
4. Auto-Deploy מופעל על כל push ל-branch הראשי (D28 — ללא Pipeline נוסף).
5. Qdrant Cloud: יצירת Cluster בנפרד (מחוץ ל-Render), חד-פעמית, לפני הרצת סקריפט האינדוקס.
6. דיפלוי ראשון מתבצע **מיד לאחר שכבה 0 עובדת מקומית** (ולא בסוף) — עיקרון "פרסי לענן מוקדם ולעתים קרובות" (מקור: ניתוח הדרישות, סעיף 23).

---

## 12. Execution Strategy

- עבודה בשכבות עולות, בדיוק לפי מבנה המסמך: 0 → 1 → 2 → 3.
- כל שכבה עוברת אימות מפורש (Definition of Done, ראו סעיף 15) **לפני** תחילת השכבה הבאה — בונוס לא נספר אם השכבה שמתחתיו שבורה.
- דיפלוי מתבצע לראשונה מיד בתום שכבה 0, ולאחר מכן מחדש (Redeploy) בתום כל שכבה נוספת שהושלמה.
- הכנת רשימת ה-URL הקבועה (~15-20 דפי FastAPI docs) והבוילרפלייט הראשוני (מבנה פרויקט, `requirements.txt`) מומלצת **לפני** תחילת שעון 90 הדקות, שכן המסמך מתיר שימוש בבוילרפלייט/Starter מוכן.
- שימוש בעוזר AI (Claude Code/Cursor) מותר ומעודד לאורך כל הביצוע, בהתאם למסמך המקור.

---

## 13. Execution Order

| # | צעד | מטרה (Goal) | תוצר (Deliverable) | תלות (Dependencies) | Definition of Done |
|---|---|---|---|---|---|
| 1 | שלד פרויקט | הקמת מבנה FastAPI בסיסי + טעינת Env Vars | אפליקציית FastAPI ריצה מקומית | — | `uvicorn` רץ מקומית, `/` מחזיר 200 |
| 2 | סכמת SQLite | יצירת טבלת `documents` לפי סעיף 7.1 | קובץ DB + לוגיקת יצירה אוטומטית של הסכימה בעליית השרת | צעד 1 | טבלה נוצרת אוטומטית בהרצה נקייה |
| 3 | `POST /ingest` | מימוש שמירת מקור בודד (URL או טקסט) | Endpoint פועל מקומית | צעד 2 | בקשה עם `url` **או** `text` שומרת רשומה; בקשה לא תקינה מחזירה 422 |
| 4 | `GET /documents` | מימוש שליפת רשימה מלאה | Endpoint פועל מקומית | צעד 3 | מחזיר את כל הרשומות שנשמרו עם תוכן מלא |
| 5 | `POST /ask` — שכבה 0 | חיפוש טקסט פשוט (SQL LIKE) | Endpoint פועל מקומית | צעד 4 | שאלה עם מילת מפתח קיימת מחזירה קטע טקסט תואם |
| 6 | **דיפלוי ראשון (שכבה 0)** | הוכחת צינור ענן חי מוקדם | URL ציבורי חי ב-Render עונה על 3 ה-Endpoints | צעדים 1-5 | פתיחת ה-URL הציבורי, קריאה ל-Endpoint, תשובה אמיתית מהמסד (תנאי המעבר של המסמך) |
| 7 | שכבה 1 — LLM חופשי | חיבור `/ask` ל-`gpt-4o-mini` (ללא Context) | `/ask` מחזיר תשובה מנוסחת מהמודל | צעד 6 | שאלה חופשית מחזירה תשובה שנוצרה ע"י LLM, מה-URL החי |
| 8 | Redeploy שכבה 1 | עדכון הענן | URL חי מעודכן | צעד 7 | בדיקה חוזרת מה-URL הציבורי |
| 9 | סקריפט אינדוקס (`scripts/index_docs.py`) | Scraping + Cleaning + Chunking + Embeddings + Qdrant upsert עבור ~15-20 URL | הרצה חד-פעמית מצליחה, Qdrant מאוכלס | צעד 8, Qdrant Cluster קיים | הרצת הסקריפט מסתיימת ללא שגיאות; מספר הצ'אנקים ב-Qdrant > 0 |
| 10 | שכבה 2 — Retrieval | חיבור `/ask` ל-Qdrant (top-4, סף 0.75) + הזרקת Context ל-LLM + ציטוט | `/ask` מחזיר תשובה מבוססת מקור עם `sources` | צעד 9 | שאלה שהתשובה לה בדוקומנטציה מחזירה תשובה נכונה + URL מקור; שאלה מחוץ לתחום מחזירה "אין לי מידע על זה" |
| 11 | Redeploy שכבה 2 | עדכון הענן | URL חי מעודכן | צעד 10 | בדיקה חוזרת מה-URL הציבורי |
| 12 | שכבה 3 — פרונט | דף צ'אט סטטי (HTML/CSS/JS) מוגש ע"י FastAPI | ממשק בדפדפן קורא ל-`/ask` ומציג תשובה+מקורות | צעד 11 | הקלדת שאלה בדפדפן ולחיצת שליחה מציגות תשובה על המסך, ללא Terminal |
| 13 | Redeploy שכבה 3 | עדכון הענן הסופי | URL חי סופי | צעד 12 | בדיקה חוזרת מה-URL הציבורי |
| 14 | בדיקת עשן | טסט אוטומטי אחד ל-`POST /ask` | קובץ טסט עובר | צעד 13 (או מוקדם יותר אם נותר זמן) | הרצת הטסט מצליחה |
| 15 | תיעוד והגשה | README, מסמך תכנון 10 הדקות, הקלטת מסך, סקיצת ארכיטקטורה | כל פריטי "מה מגישים" קיימים בריפו | כל הצעדים הקודמים לפי מה שהושלם בפועל | כל הפריטים בסעיף 19 בניתוח הדרישות קיימים |

---

## 14. Capability Breakdown

(יכולות לוגיות, לא Milestones — הפירוק לצעדי ביצוע מפורטים ייעשה בנפרד על ידי המפתח/ת)

1. **Document Ingestion** — קליטה ושמירה של מקור בודד (URL/טקסט).
2. **Document Listing** — שליפת כל המסמכים השמורים.
3. **Keyword Q&A** — מענה לשאלות בחיפוש טקסט פשוט (שכבה 0).
4. **LLM-Powered Q&A** — מענה חופשי מבוסס מודל שפה (שכבה 1).
5. **Documentation Indexing Pipeline** — סקרייפינג, ניקוי, Chunking, Embeddings, Qdrant upsert (שכבה 2).
6. **Retrieval-Augmented Q&A** — אחזור הקשר, הזרקה ל-LLM, ציטוט מקור, "אין לי מידע" (שכבה 2).
7. **Chat Frontend** — ממשק צ'אט בדפדפן (שכבה 3).
8. **Cloud Deployment & Secrets Management** — דיפלוי ל-Render, ניהול Env Vars.
9. **Quality Assurance** — בדיקת עשן ל-`/ask`.
10. **Submission Deliverables** — README, מסמך תכנון, הקלטה, סקיצת ארכיטקטורה.

---

## 15. Definition of Done

| שכבה | Definition of Done (מקור: תנאי מעבר מפורשים בניתוח הדרישות) |
|---|---|
| 0 | פתיחת ה-URL הציבורי, קריאה ל-Endpoint, קבלת תשובה אמיתית מהמסד. |
| 1 | שאלה חופשית חוזרת עם תשובה שנוצרה ע"י מודל שפה, מה-URL החי. |
| 2 | שאלה שהתשובה לה נמצאת רק בדוקומנטציה שנגרפה מקבלת תשובה נכונה עם ציטוט מקור; שאלה מחוץ לתחום מקבלת "אין לי מידע על זה". |
| 3 | הקלדת שאלה בממשק וקבלת תשובה על המסך, בלי לגעת ב-Terminal. |
| כללי (מערכת) | כל הפריטים בסעיף "מה מגישים" (README, ריפו, URL חי, מסמך תכנון, הקלטה, סקיצה) קיימים. |

---

## 16. Timeline

מבוסס על לוח הזמנים המוצע במסמך המקור (סעיף 20 בניתוח הדרישות), ממופה לצעדי סעיף 13 לעיל. זהו לוח הזמנים ל**הרצה החיה בפועל** (90 הדקות), בהנחה שהכנה מקדימה (בוילרפלייט + רשימת URL) בוצעה מראש:

| זמן | צעדים (מסעיף 13) | פלט |
|---|---|---|
| 0–10 | תכנון (מסמך זה + הפירוק הבא לצעדים קטנים) | מסמך תוכנית קצר |
| 10–40 | צעדים 1–6 (שכבה 0 + דיפלוי ראשון) | Endpoint חי עם URL ציבורי |
| 40–55 | צעדים 7–8 (שכבה 1) | תשובה חופשית מהמודל |
| 55–80 | צעדים 9–11 (שכבה 2: אינדוקס + Retrieval) | תשובה מבוססת מקור |
| 80–90 | צעדים 12–15 (שכבה 3 + בדיקת עשן + ליטוש README) — לפי זמן שנותר | הגשה מסודרת |

**הערה (Developer Attention Required):** חלון 55–80 (25 דקות) לשכבה 2 כולל הרצת סקריפט אינדוקס מלא (סקרייפינג + Embeddings בפועל ל-15-20 עמודים) בנוסף למימוש ה-Retrieval עצמו — זהו החלון הצפוף ביותר בתוכנית. מומלץ לשקול הרצה מוקדמת (Pre-run) של סקריפט האינדוקס לפני תחילת השעון הרשמי, אם כללי האתגר מתירים זאת, כדי לצמצם סיכון.

---

## 17. Risks

### סיכונים שהועברו מניתוח הדרישות (מפורשים ומשתמעים)
- דיפלוי מושאר לסוף — **מנוטרל** על ידי מיקום דיפלוי ראשון מיד אחרי שכבה 0 (צעד 6).
- התאהבות בסקרייפינג — **מנוטרל** על ידי רשימת URL קבועה מראש (D19), ללא Crawler דינמי.
- רדיפה אחרי בונוסים על חשבון הליבה — **מנוטרל** על ידי סדר ביצוע נוקשה + Definition of Done לכל שכבה.
- צ'אנקים ענקיים — **מנוטרל** על ידי מגבלת 500 טוקנים (D20).
- מפתח API בקוד — **מנוטרל** על ידי Environment Variables בלבד (D30).
- שכחה לענות "אין לי מידע" — **מנוטרל** על ידי סף Cosine Similarity מוגדר (D22).
- חשיפת עלות בלתי מבוקרת (Rate Limiting) — **לא מנוטרל, סיכון פתוח**: הוחלט במפורש להשמיט Rate Limiting עקב אילוץ זמן (D25).

### סיכונים חדשים שעלו בשלב התכנון

| # | סיכון | תיאור |
|---|---|---|
| R1 | התמדת SQLite ב-Render Free Tier | ייתכן שדיסק ה-Free Tier מתאפס ב-Redeploy (בניגוד ל-Restart). עלול לפגוע בדרישת "הנתונים שורדים ריסטארט". |
| R2 | צפיפות חלון הזמן לשכבה 2 | 25 דקות לביצוע אינדוקס מלא + Retrieval הוא החלון הצפוף ביותר בלוח הזמנים (ראו סעיף 16). |
| R3 | תלות ברשת חיצונית בזמן אמת | קריאות ל-OpenAI ול-Qdrant Cloud בזמן ההדגמה החיה תלויות בזמינות/מהירות תגובה של ספקים חיצוניים; אין Retry logic מתוכנן (מחוץ להיקף). |
| R4 | ללא Rate Limiting | `POST /ask` פתוח לציבור ומפעיל API בתשלום ללא הגנה — סיכון עלות אם ה-URL ייחשף לשימוש נרחב לאחר ההגשה. |

---

## 18. Risk Mitigation

| סיכון | פעולת מיטיגציה מוצעת |
|---|---|
| R1 — התמדת SQLite | לבדוק בפועל את התנהגות הדיסק ב-Render לפני/במהלך ההקמה; אם מתאפס ב-Redeploy — להריץ מחדש את סקריפט האינדוקס (הוא Idempotent הודות ל-`url` UNIQUE, D15) ולשקול חלופה בתשלום עם Persistent Disk אם נדרשת עמידות מלאה. |
| R2 — צפיפות שכבה 2 | הרצת סקריפט האינדוקס כהכנה מקדימה (Pre-run) לפני תחילת השעון הרשמי, אם מותר; הכנת רשימת ה-URL ובוילרפלייט מראש (מותר לפי כללי המסמך). |
| R3 — תלות רשת חיצונית | לוודא זמינות מפתחות ה-API (OpenAI, Qdrant) ותקינותם *לפני* תחילת השעון; לשקול בדיקת חיבור (Smoke Check) ידנית מוקדמת. |
| R4 — ללא Rate Limiting | לתעד ב-README כסיכון ידוע וכפריט ל"מה הייתי משפרת עם עוד זמן" (נדרש ממילא בתוצרי ההגשה); לשקול השבתת ה-URL הציבורי לאחר סיום ההערכה. |

---

## 19. Decision Traceability

כל החלטה מסעיף 4 מקושרת למקור:

- **Requirement Document:** D14, D19, D22 (חלק), D23 (חלק), D26, D30 — נגזרות ישירות מדרישה מפורשת במסמך המקור.
- **Developer Decision:** כל שאר ההחלטות (D1-D13, D15-D18, D20-D21, D24-D25, D27-D29) — נאספו בסשן שאלות-ותשובות אינטראקטיבי עם המפתח/ת, לאחר שזוהו כפערים במסמך הדרישות (סעיף 12, 15 בניתוח הדרישות).
- אין אף החלטה המסומנת כ-Assumption — כל פער נסגר באמצעות שאלה ישירה למפתח/ת, בהתאם לכללי סקיל התכנון.

---

## 20. Planning Validation Checklist

- [x] כל דרישה פונקציונלית מניתוח הדרישות (FR-1 עד FR-9) מכוסה בתוכנית (סעיפים 8, 13, 15).
- [x] כל תוצר הגשה מוגדר במפורש (README, ריפו, URL, מסמך תכנון, הקלטה, סקיצה) מופיע בצעד 15.
- [x] אין עבודת בונוס שמקדימה עבודת חובה — סדר הביצוע (סעיף 13) מתחיל משכבה 0 ודיפלוי, לפני כל שכבת בונוס.
- [x] לכל החלטה הנדסית (סעיף 4) יש מקור מתועד (Requirement Document / Developer Decision).
- [x] אין הנחה המוצגת כעובדה — כל פער נסגר בשאלה מפורשת למפתח/ת (סעיף 19).
- [x] התוכנית ניתנת למימוש ישיר: סכמת DB מלאה (סעיף 7), חוזי API מלאים (סעיף 8), סדר ביצוע עם DoD לכל צעד (סעיף 13).
- [x] התוכנית מוכנה למסירה לשלב פירוק היכולות לצעדים קטנים (Capability Planning), כבקשת המפתח/ת.

</div>
