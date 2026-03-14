from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ItemSource(BaseModel):
    tool: str = Field(description="הכלי שבו נכתב המסמך (למשל cursor, claude)")
    file: str = Field(description="נתיב הקובץ היחסי")
    anchor: Optional[str] = Field(None, description="הכותרת שתחתיה נמצא המידע")


class Decision(BaseModel):
    id: str = Field(description="מזהה ההחלטה (למשל dec-001)")
    title: str = Field(description="כותרת קצרה")
    summary: str = Field(description="תמצית ההחלטה")
    tags: List[str] = Field(default=[])
    source: ItemSource
    observed_at: str = Field(default_factory=lambda: "2026-03-15")

class Rule(BaseModel):
    id: str = Field(description="מזהה הכלל (למשל rule-001)")
    rule: str = Field(description="תיאור הכלל")
    scope: str = Field(description="תחום (ui, db, general)")
    source: ItemSource
    observed_at: str = Field(default_factory=lambda: "2026-03-15")

class WarningItem(BaseModel):
    id: str = Field(description="מזהה האזהרה")
    area: str = Field(description="אזור רלוונטי (auth, server, api)")
    message: str = Field(description="תוכן האזהרה")
    severity: str = Field(description="חומרה: high, medium, low")
    source: ItemSource
    observed_at: str = Field(default_factory=lambda: "2026-03-15")

class ProjectItems(BaseModel):
    decisions: List[Decision] = []
    rules: List[Rule] = []
    warnings: List[WarningItem] = []

class FileInfo(BaseModel):
    path: str
    last_modified: str = "2026-03-15"
    hash: str = "sha256:default"

class SourceInfo(BaseModel):
    tool: str
    root_path: str
    files: List[FileInfo]

class ExtractedProjectData(BaseModel):
    schema_version: str = "1.0"
    generated_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    sources: List[SourceInfo] = []
    items: ProjectItems