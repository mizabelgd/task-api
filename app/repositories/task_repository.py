from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskRepository:
    def create(self, db: Session, data: TaskCreate) -> Task:
        task = Task(**data.model_dump())
        db.add(task)
        db.flush()
        return task

    def get_all(self, db: Session, skip: int, limit: int) -> list[Task]:
        return db.query(Task).offset(skip).limit(limit).all()

    def get_by_id(self, db: Session, task_id: int) -> Task | None:
        return db.query(Task).filter(Task.id == task_id).first()

    def update(self, db: Session, task: Task, data: TaskUpdate) -> Task:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(task, field, value)
        db.flush()
        return task

    def delete(self, db: Session, task: Task) -> None:
        db.delete(task)
        db.flush()
