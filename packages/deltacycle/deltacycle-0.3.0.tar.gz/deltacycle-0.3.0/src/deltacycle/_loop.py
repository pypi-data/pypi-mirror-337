"""Event Loop"""

# pylint: disable=broad-exception-caught
# pylint: disable=protected-access

from __future__ import annotations

from collections.abc import Callable, Coroutine, Generator
from enum import IntEnum, auto
from typing import Any

from ._error import CancelledError, FinishError, InvalidStateError
from ._suspend_resume import SuspendResume
from ._task import Task, TaskState
from ._taskq import TaskQueue
from ._variable import Variable

type Predicate = Callable[[], bool]


def create_task(coro: Coroutine[Any, Any, Any], region: int = 0) -> Task:
    loop = get_running_loop()
    return loop.create_task(coro, region)


class LoopState(IntEnum):
    """Loop State

    Transitions::

                   +---------+
                   |         |
                   v         |
        INIT -> RUNNING -> HALTED
                        -> COMPLETED
                        -> FINISHED
    """

    # Initialized
    INIT = auto()

    # Currently running
    RUNNING = auto()

    # Halted by run limit
    HALTED = auto()

    # All tasks completed
    COMPLETED = auto()

    # finish() called
    FINISHED = auto()


class Loop:
    """Simulation event loop."""

    init_time = -1
    start_time = 0

    def __init__(self):
        """Initialize simulation."""
        self._state = LoopState.INIT

        # Simulation time
        self._time: int = self.init_time

        # Currently executing task
        self._task: Task | None = None

        # Task queue
        self._queue = TaskQueue()

        # Model variables
        self._touched: set[Variable] = set()

    def _set_state(self, state: LoopState):
        match self._state:
            case LoopState.INIT:
                assert state is LoopState.RUNNING
            case LoopState.RUNNING:
                assert state in {LoopState.HALTED, LoopState.COMPLETED, LoopState.FINISHED}
            case LoopState.HALTED:
                assert state is LoopState.RUNNING
            case _:  # pragma: no cover
                assert False
        self._state = state

    def state(self) -> LoopState:
        return self._state

    def time(self) -> int:
        return self._time

    def task(self) -> Task:
        assert self._task is not None
        return self._task

    # Scheduling methods
    def _schedule(self, time: int, task: Task, value: Any):
        task._set_state(TaskState.PENDING)
        self._queue.push(time, task, value)

    def call_soon(self, task: Task, value: Any = None):
        self._schedule(self._time, task, value)

    def call_later(self, delay: int, task: Task, value: Any = None):
        self._schedule(self._time + delay, task, value)

    def call_at(self, when: int, task: Task, value: Any = None):
        self._schedule(when, task, value)

    def create_task(self, coro: Coroutine[Any, Any, Any], region: int = 0) -> Task:
        # Cannot call create_task before the simulation starts
        assert self._time >= 0
        task = Task(coro, region)
        self.call_soon(task)
        return task

    def touch(self, v: Variable):
        self._touched.add(v)

    def _update(self):
        while self._touched:
            v = self._touched.pop()
            v.update()

    def _finish(self):
        self._set_state(LoopState.FINISHED)

    def _limit(self, ticks: int | None, until: int | None) -> int | None:
        """Determine the run limit."""
        match ticks, until:
            # Run until no tasks left
            case None, None:
                return None
            # Run until an absolute time
            case None, int():
                return until
            # Run until a number of ticks in the future
            case int(), None:
                return max(self.start_time, self._time) + ticks
            case _:
                s = "Expected either ticks or until to be int | None"
                raise TypeError(s)

    def _kernel(self, limit: int | None):
        if self._state in {LoopState.INIT, LoopState.HALTED}:
            self._set_state(LoopState.RUNNING)
        else:
            s = f"Expected state in {{INIT, HALTED}}, got {self._state.name}"
            raise InvalidStateError(s)

        while self._queue:
            # Peek when next event is scheduled
            time, _, _ = self._queue.peek()

            # Protect against time traveling tasks
            assert time > self._time

            # Exit if we hit the run limit
            if limit is not None and time >= limit:
                self._set_state(LoopState.HALTED)
                break

            # Otherwise, advance to new timeslot
            self._time = time

            # Execute time slot
            for _, task, value in self._queue.iter_time():
                self._task = task
                try:
                    task._do_run(value)
                except StopIteration as e:
                    task._do_complete(e)
                except CancelledError as e:
                    task._do_cancel(e)
                except FinishError:
                    self._finish()
                    return
                except Exception as e:
                    task._do_except(e)

            # Update simulation state
            self._update()
        else:
            self._set_state(LoopState.COMPLETED)

    def run(self, ticks: int | None = None, until: int | None = None):
        """Run the simulation.

        Until:
        1. We hit the runlimit, OR
        2. There are no tasks left in the queue
        """
        limit = self._limit(ticks, until)
        self._kernel(limit)

    def __iter__(self) -> Generator[int, None, None]:
        if self._state in {LoopState.INIT, LoopState.HALTED}:
            self._set_state(LoopState.RUNNING)
        elif self._state is not LoopState.RUNNING:
            s = f"Expected state in {{INIT, HALTED, RUNNING}}, got {self._state.name}"
            raise InvalidStateError(s)

        while self._queue:
            # Peek when next event is scheduled
            time, _, _ = self._queue.peek()

            # Protect against time traveling tasks
            assert time > self._time

            # Yield before entering new timeslot
            yield time

            # Advance to new timeslot
            self._time = time

            # Execute time slot
            for _, task, value in self._queue.iter_time():
                self._task = task
                try:
                    task._do_run(value)
                except StopIteration as e:
                    task._do_complete(e)
                except CancelledError as e:
                    task._do_cancel(e)
                except FinishError:
                    self._finish()
                    return
                except Exception as e:
                    task._do_except(e)

            # Update simulation state
            self._update()
        else:
            self._set_state(LoopState.COMPLETED)


_loop: Loop | None = None


def get_running_loop() -> Loop:
    if _loop is None:
        raise RuntimeError("No running loop")
    return _loop


def get_loop() -> Loop | None:
    """Get the current event loop."""
    return _loop


def set_loop(loop: Loop):
    """Set the current event loop."""
    global _loop
    _loop = loop


def now() -> int:
    loop = get_running_loop()
    return loop.time()


def run(
    coro: Coroutine[Any, Any, Any] | None = None,
    region: int = 0,
    loop: Loop | None = None,
    ticks: int | None = None,
    until: int | None = None,
):
    """Run a simulation."""
    if loop is None:
        set_loop(loop := Loop())
        # TODO(cjdrake): Raise an exception for this
        assert coro is not None
        task = Task(coro, region)
        loop.call_at(Loop.start_time, task)
    else:
        set_loop(loop)

    loop.run(ticks, until)


def irun(
    coro: Coroutine[Any, Any, Any] | None = None,
    region: int = 0,
    loop: Loop | None = None,
) -> Generator[int, None, None]:
    """Iterate a simulation."""
    if loop is None:
        set_loop(loop := Loop())
        # TODO(cjdrake): Raise an exception for this
        assert coro is not None
        task = Task(coro, region)
        loop.call_at(Loop.start_time, task)
    else:
        set_loop(loop)

    yield from loop


async def sleep(delay: int):
    """Suspend the task, and wake up after a delay."""
    loop = get_running_loop()
    task = loop.task()
    loop.call_later(delay, task)
    await SuspendResume()


async def changed(*vs: Variable) -> Variable:
    """Resume execution upon variable change."""
    loop = get_running_loop()
    task = loop.task()
    for v in vs:
        v.wait(task)
    task._set_state(TaskState.WAITING)
    v = await SuspendResume()
    return v


async def touched(vps: dict[Variable, Predicate | None]) -> Variable:
    """Resume execution upon variable predicate."""
    loop = get_running_loop()
    task = loop.task()
    for v, p in vps.items():
        v.wait(task, p)
    task._set_state(TaskState.WAITING)
    v = await SuspendResume()
    return v


def finish():
    raise FinishError()
