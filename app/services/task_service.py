from sqlalchemy.orm import Session

from app.models.task import Task
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate

_repo = TaskRepository()


class TaskService:
    def create_task(self, db: Session, data: TaskCreate, user_id: int) -> Task:
        task = _repo.create(db, data, user_id)
        db.commit()
        db.refresh(task)
        return task

    def list_tasks(self, db: Session, user_id: int, skip: int, limit: int) -> list[Task]:
        return _repo.get_all(db, user_id, skip, limit)

    def get_task(self, db: Session, task_id: int, user_id: int) -> Task | None:
        return _repo.get_by_id(db, task_id, user_id)

    def update_task(
        self, db: Session, task_id: int, data: TaskUpdate, user_id: int
    ) -> Task | None:
        task = _repo.get_by_id(db, task_id, user_id)
        if task is None:
            return None
        task = _repo.update(db, task, data)
        db.commit()
        db.refresh(task)
        return task

    def delete_task(self, db: Session, task_id: int, user_id: int) -> bool:
        task = _repo.get_by_id(db, task_id, user_id)
        if task is None:
            return False
        _repo.delete(db, task)
        db.commit()
        return True
