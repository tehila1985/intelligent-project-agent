# Security and Compliance Policy

## Decisions
- **dec-sec-001**: שימוש ב-OAuth2 עם JWT לניהול הזדהות משתמשים.
- **dec-sec-002**: בחירה ב-Auth0 כספק הזהויות החיצוני (IDP).

## Rules
- **rule-auth-001**: תוקף של Access Token לא יעלה על 15 דקות.
- **rule-auth-002**: חובה להפעיל MFA (אימות דו-שלבי) לכל משתמש בעל הרשאות Admin.

## Warnings
- **warn-auth-001**: חשיפת ה-Secret Key של ה-JWT תאפשר זיוף טוקנים. חובה להחליף מפתח כל 90 יום.