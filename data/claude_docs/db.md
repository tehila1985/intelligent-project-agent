# Database Architecture and Strategy

## Decisions
- **dec-001**: שימוש ב-Postgres כבסיס הנתונים הראשי (Relational) עבור ניהול משתמשים ועסקאות. נבחר בשל התמיכה ב-ACID compliance. #db-core
- **dec-002**: הטמעת Pinecone כ-Vector Database עבור אחסון ה-Embeddings של מסמכי הפרויקט. נבחר בשל יכולת ה-Scaling המהירה. #rag-infra
- **dec-003**: שימוש ב-Redis כשכבת Caching עבור שאילתות חוזרות של ה-LLM כדי לחסוך בעלויות API. #performance

## Rules
- **rule-db-001**: חובה להשתמש ב-Migration scripts (Alembic/Prisma) לכל שינוי בסכימה. אין לבצע Alter Table ידני.
- **rule-db-002**: כל שאילתה ל-Postgres חייבת לעבור דרך שכבת ה-Repository, אין לכתוב שאילתות SQL ישירות ב-Workflow.
- **rule-db-003**: נתונים רגישים (PII) חייבים להיות מוצפנים ברמת העמודה (Encryption at rest).

## Warnings
- **warn-db-001**: שים לב! בסיס הנתונים ב-Staging מוגבל ל-1GB. מחיקת נתונים ישנים מתבצעת כל יום ראשון. #critical