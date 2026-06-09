from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout, QWidget

from watchwidget.config import COLORS, LEFT_PANEL_WIDTH, ROW_HEIGHT
from watchwidget.models import City, ScrubberState
from watchwidget.services.timezone import (
    format_clock,
    local_datetime_for_reference_hour,
    now_for_city,
    offset_from_reference,
    timezone_abbreviation,
)
from watchwidget.widgets.timeline_canvas import TimelineCanvas


class TimelineRow(QFrame):
    def __init__(self, city: City, scrubber: ScrubberState, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._city = city
        self._scrubber = scrubber

        self.setObjectName("timelineRow")
        self.setMinimumHeight(ROW_HEIGHT)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self._name_label = QLabel(city.name)
        self._name_label.setObjectName("cityName")
        self._meta_label = QLabel()
        self._meta_label.setObjectName("cityMeta")
        self._time_label = QLabel()
        self._time_label.setObjectName("cityTime")
        self._selected_label = QLabel()
        self._selected_label.setObjectName("selectedTime")

        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(10, 3, 4, 3)
        left_layout.setSpacing(0)
        left_layout.addWidget(self._name_label)
        left_layout.addWidget(self._meta_label)

        time_layout = QVBoxLayout()
        time_layout.setContentsMargins(0, 3, 10, 3)
        time_layout.setSpacing(0)
        time_layout.addWidget(self._time_label, alignment=Qt.AlignmentFlag.AlignRight)
        time_layout.addWidget(self._selected_label, alignment=Qt.AlignmentFlag.AlignRight)

        left_panel = QWidget()
        left_panel.setFixedWidth(LEFT_PANEL_WIDTH)
        left_panel.setLayout(left_layout)

        time_panel = QWidget()
        time_panel.setFixedWidth(78)
        time_panel.setLayout(time_layout)

        self._canvas = TimelineCanvas(city, scrubber, self)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(left_panel)
        layout.addWidget(time_panel)
        layout.addWidget(self._canvas, stretch=1)

        self._scrubber.position_changed.connect(lambda _hour: self.refresh())
        self.refresh()

    def refresh(self) -> None:
        now = now_for_city(self._city)
        selected = local_datetime_for_reference_hour(self._city, self._scrubber.hour)
        abbreviation = timezone_abbreviation(self._city)
        offset = offset_from_reference(self._city)

        self._meta_label.setText(f"{offset} {abbreviation}".strip())
        self._time_label.setText(format_clock(now))
        self._selected_label.setText(format_clock(selected))

    @staticmethod
    def stylesheet() -> str:
        return f"""
        QFrame#timelineRow {{
            background: {COLORS["panel_bg"]};
            border-bottom: 1px solid {COLORS["border"]};
        }}
        QLabel#cityName {{
            color: {COLORS["text"]};
            font-size: 14px;
            font-weight: 700;
        }}
        QLabel#cityMeta, QLabel#selectedTime {{
            color: {COLORS["muted"]};
            font-size: 10px;
        }}
        QLabel#cityTime {{
            color: {COLORS["text"]};
            font-size: 14px;
            font-weight: 700;
        }}
        """
