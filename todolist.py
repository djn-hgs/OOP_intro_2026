from datetime import date


class Task:
    def __init__(self, id: int, title: str, due_date: date | None = None):
        raise NotImplementedError

    def complete(self) -> None:
        raise NotImplementedError

    def is_overdue(self, today: date | None = None) -> bool:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError


class TodoList:
    def __init__(self):
        raise NotImplementedError

    def add(self, title: str, due_date: date | None = None) -> Task:
        raise NotImplementedError

    def get(self, task_id: int) -> Task:
        raise NotImplementedError

    def complete(self, task_id: int) -> None:
        raise NotImplementedError

    def remove(self, task_id: int) -> None:
        raise NotImplementedError

    def list(self, done: bool | None = None) -> list[Task]:
        raise NotImplementedError

    def overdue(self, today: date | None = None) -> list[Task]:
        raise NotImplementedError

    def sorted_by_due(self) -> list[Task]:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError
