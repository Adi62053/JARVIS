import os
import time
from dataclasses import dataclass
from typing import Optional

import psutil


@dataclass(frozen=True)
class ResourceSnapshot:
    cpu_percent: float
    memory_percent: float
    memory_total_bytes: int
    memory_available_bytes: int
    process_cpu_percent: float
    process_memory_bytes: int
    process_thread_count: int
    cpu_count: int


class ResourceManager:
    """Read-only resource monitoring for JARVIS V10.6."""

    def __init__(self, process: Optional[psutil.Process] = None):
        self._process = process or psutil.Process(os.getpid())

        # Establish CPU measurement baselines.
        psutil.cpu_percent(interval=None)
        self._process.cpu_percent(interval=None)

    def snapshot(self) -> ResourceSnapshot:
        memory = psutil.virtual_memory()

        return ResourceSnapshot(
            cpu_percent=psutil.cpu_percent(interval=None),
            memory_percent=memory.percent,
            memory_total_bytes=memory.total,
            memory_available_bytes=memory.available,
            process_cpu_percent=self._process.cpu_percent(interval=None),
            process_memory_bytes=self._process.memory_info().rss,
            process_thread_count=self._process.num_threads(),
            cpu_count=psutil.cpu_count() or 1,
        )

    def sample(self, interval: float = 1.0) -> ResourceSnapshot:
        if interval <= 0:
            raise ValueError("interval must be greater than zero")

        # Establish synchronized CPU measurement baselines.
        psutil.cpu_percent(interval=None)
        self._process.cpu_percent(interval=None)

        time.sleep(interval)

        cpu_percent = psutil.cpu_percent(interval=None)
        process_cpu_percent = self._process.cpu_percent(interval=None)
        memory = psutil.virtual_memory()

        return ResourceSnapshot(
            cpu_percent=cpu_percent,
            memory_percent=memory.percent,
            memory_total_bytes=memory.total,
            memory_available_bytes=memory.available,
            process_cpu_percent=process_cpu_percent,
            process_memory_bytes=self._process.memory_info().rss,
            process_thread_count=self._process.num_threads(),
            cpu_count=psutil.cpu_count() or 1,
        )

    def get_process_id(self) -> int:
        return self._process.pid
