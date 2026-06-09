from __future__ import annotations

from dataclasses import dataclass
from datetime import tzinfo

from PySide6.QtCore import QObject, Signal


@dataclass(frozen=True, slots=True)
class City:
    name: str
    timezone: tzinfo


class ScrubberState(QObject):
    position_changed = Signal(int)

    def __init__(self, initial_hour: int = 0, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._hour = initial_hour % 24

    @property
    def hour(self) -> int:
        return self._hour

    def set_hour(self, hour: int) -> None:
        normalized = max(0, min(23, int(hour)))
        if normalized == self._hour:
            return

        self._hour = normalized
        self.position_changed.emit(self._hour)
