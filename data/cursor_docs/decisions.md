# Global Project Guidelines & System Logic

## Infrastructure Decisions
- **dec-infra-001**: שימוש ב-FastAPI כשרת ה-Backend המרכזי בשל התמיכה המובנית ב-Asyncio.
- **dec-infra-002**: בחירה ב-Cohere Command-R כמודל ה-LLM המרכזי (Production) בשל חלון הקשר גדול (128k) ועלויות נמוכות.
- **dec-infra-003**: אימוץ ארכיטקטורת Event-Driven Workflow (באמצעות LlamaIndex Workflows) לניהול הלוגיקה של הסוכן.

## UI/UX Rules
- **rule-ui-001**: כל הממשק חייב להיות נגיש (Accessibility Level AA).
- **rule-ui-002**: תמיכה מלאה ב-RTL (עברית/ערבית) היא תנאי סף לכל קומפוננטה חדשה.
- **rule-ui-003**: שימוש ב-Tailwind CSS בלבד עבור עיצובים, אין להשתמש ב-Inline Styles.

## Security & API Warnings
- **warn-sec-001**: אין להעלות קבצי `.env` ל-GitHub. חובה להשתמש ב-Secrets Manager בסביבת ה-Production.
- **warn-api-002**: מגבלת קצב (Rate Limit) ל-Cohere API עומדת על 5 קריאות בשנייה בחשבון ה-Trial. שימוש מוגבר יגרור שגיאת 429.
- **warn-api-003**: זהירות בעבודה עם `model_dump_json` - יש לוודא שאין אובייקטים מסוג Datetime ללא המרה למחרוזת (ISO 8601).