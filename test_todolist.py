from datetime import date, timedelta

import pytest

from todolist import Task, TodoList

TODAY = date.today()
YESTERDAY = TODAY - timedelta(days=1)
TOMORROW = TODAY + timedelta(days=1)


# ---------- Task ----------

class TestTask:
    def test_defaults(self):
        t = Task(1, "buy milk")
        assert (t.id, t.title, t.due_date, t.done) == (1, "buy milk", None, False)

    def test_title_is_stripped(self):
        assert Task(1, "  padded  ").title == "padded"

    @pytest.mark.parametrize("bad", ["", "   ", "\t\n"])
    def test_empty_title_rejected(self, bad):
        with pytest.raises(ValueError):
            Task(1, bad)

    def test_due_date_stored(self):
        assert Task(1, "a", TOMORROW).due_date == TOMORROW

    @pytest.mark.parametrize("bad", ["2026-10-13", 20261013, 1.5])
    def test_non_date_due_date_rejected(self, bad):
        with pytest.raises(TypeError):
            Task(1, "a", bad)

    def test_complete(self):
        t = Task(1, "a")
        t.complete()
        assert t.done is True

    def test_complete_is_idempotent(self):
        t = Task(1, "a")
        t.complete()
        t.complete()
        assert t.done is True


class TestTaskOverdue:
    @pytest.mark.parametrize(
        "due, expected",
        [(YESTERDAY, True), (TODAY, False), (TOMORROW, False), (None, False)],
    )
    def test_overdue_by_date(self, due, expected):
        assert Task(1, "a", due).is_overdue(TODAY) is expected

    def test_completed_task_never_overdue(self):
        t = Task(1, "a", YESTERDAY)
        t.complete()
        assert t.is_overdue(TODAY) is False

    def test_defaults_to_real_today(self):
        assert Task(1, "a", date.today() - timedelta(days=1)).is_overdue() is True
        assert Task(1, "a", date.today()).is_overdue() is False


# ---------- TodoList ----------

@pytest.fixture
def todo():
    return TodoList()


@pytest.fixture
def populated(todo):
    todo.add("buy milk", TOMORROW)         # id 1
    todo.add("write tests", YESTERDAY)     # id 2
    todo.add("walk dog")                   # id 3
    todo.add("pay rent", YESTERDAY)        # id 4
    todo.complete(4)
    return todo


class TestAdd:
    def test_returns_task_instance(self, todo):
        task = todo.add("buy milk", TOMORROW)
        assert isinstance(task, Task)
        assert task.due_date == TOMORROW

    def test_due_date_optional(self, todo):
        assert todo.add("a").due_date is None

    def test_ids_unique_and_increasing(self, todo):
        assert [todo.add(x).id for x in "abc"] == [1, 2, 3]

    def test_invalid_task_not_added(self, todo):
        with pytest.raises(ValueError):
            todo.add("   ")
        assert len(todo) == 0

    def test_ids_not_reused_after_removal(self, todo):
        first = todo.add("a")
        todo.remove(first.id)
        assert todo.add("b").id != first.id


class TestGetCompleteRemove:
    def test_get(self, populated):
        assert populated.get(1).title == "buy milk"

    def test_complete_marks_task(self, todo):
        task = todo.add("a")
        todo.complete(task.id)
        assert task.done is True

    def test_remove(self, populated):
        populated.remove(1)
        assert len(populated) == 3
        with pytest.raises(KeyError):
            populated.get(1)

    def test_double_remove_fails(self, todo):
        task = todo.add("a")
        todo.remove(task.id)
        with pytest.raises(KeyError):
            todo.remove(task.id)


class TestList:
    def test_empty(self, todo):
        assert todo.list() == []

    def test_insertion_order(self, populated):
        assert [t.id for t in populated.list()] == [1, 2, 3, 4]

    @pytest.mark.parametrize("done, ids", [(True, [4]), (False, [1, 2, 3])])
    def test_filter_by_status(self, populated, done, ids):
        assert [t.id for t in populated.list(done=done)] == ids

    def test_list_is_a_copy(self, populated):
        populated.list().clear()
        assert len(populated) == 4


class TestOverdue:
    def test_only_incomplete_past_due(self, populated):
        assert [t.id for t in populated.overdue(TODAY)] == [2]

    def test_none_overdue(self, todo):
        todo.add("a", TOMORROW)
        todo.add("b")
        assert todo.overdue(TODAY) == []

    def test_completing_removes_from_overdue(self, populated):
        populated.complete(2)
        assert populated.overdue(TODAY) == []


class TestSortedByDue:
    def test_soonest_first_undated_last(self, populated):
        assert [t.id for t in populated.sorted_by_due()] == [2, 4, 1, 3]

    def test_stable_for_equal_dates(self, todo):
        a = todo.add("a", TODAY)
        b = todo.add("b", TODAY)
        assert todo.sorted_by_due() == [a, b]

    def test_does_not_reorder_underlying_list(self, populated):
        populated.sorted_by_due()
        assert [t.id for t in populated.list()] == [1, 2, 3, 4]

    def test_empty(self, todo):
        assert todo.sorted_by_due() == []


def test_len(populated):
    assert len(populated) == 4
