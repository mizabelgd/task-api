from sqlalchemy.orm import Session

from app.models.task import Task
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate

_repo = TaskRepository()


class TaskService:
    def create_task(self, db: Session, data: TaskCreate, user_id: int) -> Task:
        """Cria uma nova tarefa associada ao usuário e persiste no banco."""
        task = _repo.create(db, data, user_id)
        db.commit()
        db.refresh(task)
        return task

    def list_tasks(self, db: Session, user_id: int, skip: int, limit: int) -> list[Task]:
        """Retorna página de tarefas do usuário conforme skip/limit."""
        return _repo.get_all(db, user_id, skip, limit)

    def count_tasks(self, db: Session, user_id: int) -> int:
        """Retorna o total de tarefas do usuário, independente de paginação."""
        return _repo.count_all(db, user_id)

    def get_task(self, db: Session, task_id: int, user_id: int) -> Task | None:
        """Busca uma tarefa pelo ID garantindo que pertence ao usuário. Retorna None se não encontrada."""
        return _repo.get_by_id(db, task_id, user_id)

    def update_task(
        self, db: Session, task_id: int, data: TaskUpdate, user_id: int
    ) -> Task | None:
        """Aplica atualização parcial em uma tarefa do usuário. Retorna None se não encontrada."""
        task = _repo.get_by_id(db, task_id, user_id)
        if task is None:
            return None
        task = _repo.update(db, task, data)
        db.commit()
        db.refresh(task)
        return task

    def delete_task(self, db: Session, task_id: int, user_id: int) -> bool:
        """Remove uma tarefa do usuário. Retorna False se não encontrada."""
        task = _repo.get_by_id(db, task_id, user_id)
        if task is None:
            return False
        _repo.delete(db, task)
        db.commit()
        return True
