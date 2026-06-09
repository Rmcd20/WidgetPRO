from __future__ import annotations

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QFont, QMouseEvent, QPainter, QPen
from PySide6.QtWidgets import QSizePolicy, QWidget

from watchwidget.config import COLORS, HOUR_COUNT
from watchwidget.models import City, ScrubberState
from watchwidget.services.timezone import (
    format_hour_label,
    hour_is_daylight,
    local_datetime_for_reference_hour,
)


class TimelineCanvas(QWidget):
    def __init__(self, city: City, scrubber: ScrubberState, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._city = city
        self._scrubber = scrubber
        self._dragging = False
        self.setMinimumHeight(36)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._scrubber.position_changed.connect(lambda _hour: self.update())

    def paintEvent(self, _event) -> None:  # noqa: N802 - Qt API
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)
        painter.setFont(QFont("Segoe UI", 9, QFont.Weight.DemiBold))

        width = max(1, self.width())
        height = max(1, self.height())
        cell_width = width / HOUR_COUNT

        border_pen = QPen(QColor(COLORS["border"]))
        border_pen.setWidth(1)
        painter.setPen(border_pen)

        for hour in range(HOUR_COUNT):
            x = hour * cell_width
            rect = QRectF(x, 0, cell_width + 0.5, height)
            is_daylight = hour_is_daylight(self._city, hour)
            color_key = "day" if is_daylight else "night"
            painter.fillRect(rect, QColor(COLORS[color_key]))
            painter.drawRect(rect)

            local = local_datetime_for_reference_hour(self._city, hour)
            text_color = COLORS["hour_text"] if is_daylight else COLORS["hour_text_night"]
            painter.setPen(QColor(text_color))
            painter.drawText(
                rect.adjusted(0, 0, 0, 0),
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter,
                format_hour_label(local.hour),
            )
            painter.setPen(border_pen)

        self._paint_scrubber(painter, cell_width, height)

    def mousePressEvent(self, event: QMouseEvent) -> None:  # noqa: N802 - Qt API
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = True
            self._set_hour_from_x(event.position().x())
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:  # noqa: N802 - Qt API
        if self._dragging and event.buttons() & Qt.MouseButton.LeftButton:
            self._set_hour_from_x(event.position().x())
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:  # noqa: N802 - Qt API
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = False
            event.accept()

    def _set_hour_from_x(self, x: float) -> None:
        cell_width = max(1.0, self.width() / HOUR_COUNT)
        hour = int(max(0, min(HOUR_COUNT - 1, x // cell_width)))
        self._scrubber.set_hour(hour)

    def _paint_scrubber(self, painter: QPainter, cell_width: float, height: int) -> None:
        hour = self._scrubber.hour
        x = hour * cell_width
        rect = QRectF(x, 0, cell_width, height)
        painter.fillRect(rect, QColor(COLORS["scrubber_fill"]))

        pen = QPen(QColor(COLORS["scrubber"]))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawRect(rect.adjusted(1, 1, -1, -1))
