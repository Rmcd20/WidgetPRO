from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QMouseEvent, QPainter
from PySide6.QtWidgets import QSizePolicy, QWidget

from watchwidget.config import COLORS, HOUR_COUNT
from watchwidget.services.timezone import format_hour_label


class HourHeader(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._drag_start = None
        self.setMinimumHeight(28)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setCursor(Qt.CursorShape.SizeAllCursor)

    def paintEvent(self, _event) -> None:  # noqa: N802 - Qt API
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)
        painter.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        painter.fillRect(self.rect(), QColor(COLORS["window_bg"]))

        cell_width = max(1.0, self.width() / HOUR_COUNT)
        painter.setPen(QColor(COLORS["header_text"]))
        for hour in range(HOUR_COUNT):
            x = int(hour * cell_width)
            painter.drawText(
                x,
                0,
                int(cell_width),
                self.height(),
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter,
                format_hour_label(hour),
            )

    def mousePressEvent(self, event: QMouseEvent) -> None:  # noqa: N802 - Qt API
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:  # noqa: N802 - Qt API
        if self._drag_start is None or not event.buttons() & Qt.MouseButton.LeftButton:
            return

        window = self.window()
        current = event.globalPosition().toPoint()
        window.move(window.pos() + current - self._drag_start)
        self._drag_start = current
        event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:  # noqa: N802 - Qt API
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start = None
            event.accept()
