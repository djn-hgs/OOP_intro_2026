from datetime import date


class Task:
    def __init__(self, id: int, title: str, due_date: date | None = None):
        self.id = id

        self.title = title.strip()

        if self.title == "":
            raise ValueError("Task title cannot be an empty string")

        if due_date:
            if not isinstance(due_date, date):
                raise TypeError("Task due date must be of type date")

        self.due_date = due_date
        self.done = False

    def complete(self) -> None:
        if not self.done:
            self.done = True


    def is_overdue(self, today: date | None = None) -> bool:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f'{self.due_date} - {self.title} - {"Complete" if self.done else "Not complete"}'


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
