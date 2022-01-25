from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, schemas, models
from .database import SessionLocal, engine
from .helpers import db_data_to_task

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return "Welcome to Schedule API." \
           "Visit /docs to get the documentation"


# subjects
@app.get("/subjects", response_model=List[schemas.Subject])
def get_subjects(db: Session = Depends(get_db)):
    return crud.get_subjects(db)


@app.get("/subjects/{subject_id}", response_model=schemas.Subject)
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    db_subject = crud.get_subject(db, subject_id=subject_id)
    if db_subject is None:
        raise HTTPException(status_code=404, detail="This subject doesn't exist")

    return db_subject


@app.post("/subjects/add", response_model=schemas.Subject)
def add_subject(subject: schemas.SubjectCreate, db: Session = Depends(get_db)) -> schemas.Subject:
    db_subject = crud.get_subject_by_label(db, label=subject.label)
    if db_subject:
        raise HTTPException(status_code=400, detail="This subject already exist")
    db_subject = crud.insert_subject(db, subject=subject)

    return db_subject


@app.put("/subjects/update", response_model=schemas.Subject)
def update_subject(subject: schemas.SubjectUpdate, db: Session = Depends(get_db)) -> schemas.Subject:
    db_subject = crud.get_subject(db, subject_id=subject.id)
    if not db_subject:
        raise HTTPException(status_code=404, detail="This subject doesn't exist")

    return crud.update_subject(db, db_task=db_subject, new_data=subject)


@app.delete("/subjects/delete/{subject_id}")
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    db_subject = crud.get_subject(db, subject_id=subject_id)
    if db_subject is None:
        raise HTTPException(status_code=404, detail="This subject doesn't exist")

    crud.delete_subject(db, db_subject=db_subject)

    return True


# Tasks
@app.get("/tasks", response_model=List[schemas.Task])
def get_tasks(db: Session = Depends(get_db)):
    rows = crud.get_tasks(db)
    return [db_data_to_task(row) for row in rows]


@app.get("/tasks/{task_id}", response_model=schemas.Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="This task doesn't exist")

    return db_task


@app.post("/tasks/add", response_model=schemas.Task)
def add_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    added_task = crud.insert_task(db, data=task)
    print(f"##### added task {added_task}")
    return db_data_to_task(added_task)


@app.put("/tasks/update", response_model=schemas.Task)
def update_task(task: schemas.Task, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task.id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="This task doesn't exist")

    return crud.update_task(db, db_task=db_task, new_data=task)


@app.delete("/tasks/delete/{task_id}", response_model=bool)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="This task doesn't exist")

    crud.delete_task(db, db_task=db_task)

    return True
