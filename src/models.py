from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from .database import Base
from .types import DayEnum


class SubjectEntity(Base):
    __tablename__ = "subject"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, unique=True, nullable=False, index=True)
    color = Column(String)
    archived = Column(Boolean, nullable=False, default=False, )
    ts = Column(DateTime, nullable=False, default=text("current_timestamp"))

    tasks = relationship("TaskEntity", back_populates="subject")


class TaskEntity(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    description = Column(Text)
    subject_id = Column(Integer, ForeignKey("subject.id"), nullable=False)
    day = Column(Enum(DayEnum), nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    archived = Column(Boolean, nullable=False, default=False)
    ts = Column(DateTime, nullable=False, default=text("current_timestamp"))

    subject = relationship("SubjectEntity", back_populates="tasks")
