import asyncio
import logging
import sys
from asyncio import Task
from typing import Awaitable, Callable, Collection, Dict, Tuple

from metrology import Metrology

_logger = logging.getLogger(__name__)


class TasksMixin:
    """Helpers for task management."""

    tasks: Dict[str, Task] = {}
    connected: bool

    async def reset_tasks(self):
        """Cancel all tracked tasks and reset the index."""
        if self.tasks:
            # stop all background tasks
            _logger.debug(f'Cancelling tasks {", ".join(self.tasks.keys())}')
            tasks = self.tasks.values()
            if sys.version_info < (3, 9):
                [t.cancel() for t in tasks]
            else:
                [t.cancel('reset_tasks') for t in tasks]
            result = await asyncio.gather(*tasks, return_exceptions=True)
            _logger.debug(f'Result: {result}')
        self.tasks = {}

    def run_tasks_forever(self, *funcs: Tuple[Callable[[], Awaitable], float]) -> Collection[Task]:
        """Helper method to wrap coros in tasks, run them in a permanent loop and handle cancellation."""

        async def coro(f: Callable[[], Awaitable], s: float, n: str):
            while self.connected:
                try:
                    with Metrology.utilization_timer(f'time-{n}'):
                        await f()
                    await asyncio.sleep(s)
                except asyncio.CancelledError:
                    self.connected = False
                    _logger.debug(f"{n}() cancelled")
                    raise
                except asyncio.TimeoutError:
                    self.connected = False
                    _logger.error(f"{n}() timeout")
                    raise
            _logger.debug(f"{n}() stopped")

        for func, sleep in funcs:
            func_name = func.__name__
            _logger.debug(f"Forever running {func_name}()")
            if sys.version_info < (3, 8):
                self.tasks[func_name] = asyncio.create_task(coro(func, sleep, func_name))
            else:
                self.tasks[func_name] = asyncio.create_task(coro(func, sleep, func_name), name=func_name)
        return self.tasks.values()

    #########################################################################################################
    async def log_stats(self):
        """Log stats from Metrology."""
        from metrology import registry

        counters = []
        timers = []
        for name, data in registry:
            if name.startswith('time-'):
                timers.append(f'{name[5:]}={data.mean:.2f}')
                counters.append(f'{name[5:]}()={data.count}')
            else:
                counters.append(f'{name}={data.count}')
        if counters:
            print(f"counters: {' '.join(counters)}")
        if timers:
            print(f"timers: {' '.join(timers)}")
