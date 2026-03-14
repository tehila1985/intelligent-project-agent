import json
import asyncio
from pathlib import Path
from utils import load_env, get_cohere_api_key
from schema_models import ExtractedProjectData, SourceInfo, FileInfo, ProjectItems
from llama_index.llms.cohere import Cohere
from llama_index.core.program import LLMTextCompletionProgram

load_env()

# שימוש במודל command-r (הוא יציב מאוד לחילוץ בגרסת ה-Trial)
llm = Cohere(api_key=get_cohere_api_key(), model="command-r-08-2024")

async def extract_structured_data():
    print("🛠️  מתחיל חילוץ נתונים מובנים...")
    
    prompt_template_str = """
    עבור הטקסט הבא ממסמכי הפרויקט, חלץ את כל ההחלטות הטכניות (decisions), 
    הכללים (rules) והאזהרות (warnings) לפי הסכימה הנדרשת.
    
    טקסט מקור:
    {desktop_text}
    """
    
    # הגדרת התוכנית
    program = LLMTextCompletionProgram.from_defaults(
        output_cls=ExtractedProjectData,
        prompt_template_str=prompt_template_str,
        llm=llm
    )

    # יצירת אובייקט ריק לפי המבנה שביקשת (items הוא אובייקט, לא מילון)
    all_data = ExtractedProjectData(
        sources=[], 
        items=ProjectItems(decisions=[], rules=[], warnings=[])
    )
    
    data_path = Path("data")
    for file_path in data_path.rglob("*.md"):
        print(f"📄 סורק את: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        try:
            # חילוץ
            result = await program.acall(desktop_text=content)
            
            # עדכון מקורות
            all_data.sources.append(SourceInfo(
                tool="manual_scan",
                root_path=str(data_path),
                files=[FileInfo(path=str(file_path), last_modified="2026-03-15")]
            ))
            
            # איחוד פריטים
            all_data.items.decisions.extend(result.items.decisions)
            all_data.items.rules.extend(result.items.rules)
            all_data.items.warnings.extend(result.items.warnings)
            
        except Exception as e:
            print(f"⚠️ שגיאה בקובץ {file_path}: {e}")

    # שמירה לקובץ - התיקון עבור Pydantic V2
    output_file = "extracted_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        # משתמשים ב-model_dump_json במקום ב-.json()
        json_data = all_data.model_dump_json(indent=2)
        f.write(json_data)
    
    print(f"✅ הצלחנו! בדקי את הקובץ: {output_file}")

if __name__ == "__main__":
    asyncio.run(extract_structured_data())