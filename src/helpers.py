from typing import Dict
from .models import SubjectEntity, TaskEntity
from .schemas import Subject, Task


def merge_dict(old_dict: Dict, new_dict: Dict) -> Dict:
    # print(f"old dict {old_dict}")
    # print(f"new dict {new_dict}")
    for key in old_dict:
        if key in new_dict:
            try:
                # old_dict[key] = new_dict[key]
                setattr(old_dict, key, new_dict[key])
            except AttributeError as error:
                print(f"###### [AttributeError] : {error}")

    return old_dict


def db_data_to_subject(row: SubjectEntity) -> Subject:
    return Subject(
        id=row.id,
        label=row.label,
        color=row.color,
        archived=row.archived,
        ts=row.ts
    )


def db_data_to_task(row: TaskEntity) -> Task:
    return Task(
        id=row.id,
        subject_id=row.subject_id,
        description=row.description,
        day=row.day,
        start_time=row.start_time,
        end_time=row.end_time,
        archived=row.archived,
        ts=row.ts,
        subject=row.subject
    )
