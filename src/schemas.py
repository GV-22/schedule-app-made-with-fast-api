from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from .types import DayEnum

class SubjectBase(BaseModel):
    label: str
    color: str


class SubjectCreate(SubjectBase):
    pass

class SubjectUpdate(SubjectBase):
    id: int
    archived: bool

class Subject(SubjectBase):
    id: int
    archived: bool
    ts: datetime

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    day: DayEnum  # mondeay | tuesday | wednesday | ... | sunday
    description: Optional[str] = None
    start_time: str
    end_time: str
    subject_id: int

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    id: int
    archived: bool

class Task(TaskBase):
    id: int
    archived: bool
    ts: datetime
    subject: Subject

    class Conifg:
        orm_mode = True
