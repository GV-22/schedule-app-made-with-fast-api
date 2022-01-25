from fastapi.encoders import jsonable_encoder
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.exc import StatementError
from sqlite3 import IntegrityError

from . import models, schemas


def get_subjects(db: Session) -> List[models.SubjectEntity]:
    return db.query(models.SubjectEntity).all()


def get_subject(db: Session, subject_id: int) -> models.SubjectEntity:
    return db.query(models.SubjectEntity).filter(models.SubjectEntity.id == subject_id).first()


def get_subject_by_label(db: Session, label: str) -> models.SubjectEntity:
    return db.query(models.SubjectEntity).filter(models.SubjectEntity.label == label).first()


def insert_subject(db: Session, subject: schemas.SubjectCreate) -> models.SubjectEntity:
    db_subject = models.SubjectEntity(**subject.dict())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)

    return db_subject


def update_subject(db: Session, db_task: schemas.Subject, new_data: schemas.SubjectUpdate) -> models.SubjectEntity:
    obj_data = jsonable_encoder(db_task)
    if isinstance(new_data, dict):
        new_data_dict = new_data
    else:
        new_data_dict = new_data.dict(exclude_unset=True)

    try:
        for field in obj_data:
            if field in new_data_dict:
                setattr(db_task, field, new_data_dict[field])

        db.add(db_task)
        db.commit()
        db.refresh(db_task)

        return db_task
    except UnmappedInstanceError as error:
        print(f"### [UnmappedInstanceError] error: {error}")
    except StatementError as error:
        print(f"### [StatementError] error: {error}")


def delete_subject(db: Session, db_subject: models.SubjectEntity):
    try:
        db.delete(db_subject)
        db.commit()
    except IntegrityError as error:
        print(f"### [IntegrityError] error: {error}")


def archive_or_unarchive_subject(db: Session, subject: schemas.Subject) -> models.SubjectEntity:
    db_subject = models.SubjectEntity(**subject.dict(), archived=False if subject.archived else True)
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)

    return db_subject


# tasks
def get_tasks(db: Session) -> List[models.TaskEntity]:
    return db.query(models.TaskEntity).all()


def get_task(db: Session, task_id: int) -> models.TaskEntity:
    return db.query(models.TaskEntity).filter(models.TaskEntity.id == task_id).first()


def insert_task(db: Session, data: schemas.TaskCreate) -> models.TaskEntity:
    db_task = models.TaskEntity(**data.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


def update_task(db: Session, db_task: schemas.Task, new_data: schemas.Task) -> models.TaskEntity:
    obj_data = jsonable_encoder(db_task)
    if isinstance(new_data, dict):
        new_data_dict = new_data
    else:
        new_data_dict = new_data.dict(exclude_unset=True)

    try:
        for field in obj_data:
            if field in new_data_dict:
                setattr(db_task, field, new_data_dict[field])

        db.add(db_task)
        db.commit()
        db.refresh(db_task)

    except UnmappedInstanceError as error:
        print(f"### [UnmappedInstanceError] error: {error}")
    except StatementError as error:
        print(f"### [StatementError] error: {error}")

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


def delete_task(db: Session, db_task: models.TaskEntity):
    db.delete(db_task)
    db.commit()


def archive_or_unarchive_task(db: Session, task: schemas.Subject) -> models.TaskEntity:
    db_task = models.SubjectEntity(**task.dict(), archived=False if task.archived else True)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task
