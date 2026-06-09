from __future__ import annotations

from PySide6.QtCore import QEvent, QTimer, Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget, QMainWindow

from watchwidget.config import (
    CITIES,
    COLORS,
    LEFT_PANEL_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    WINDOW_X,
    WINDOW_Y,
)
from watchwidget.desktop.win32 import pin_to_desktop
from watchwidget.models import ScrubberState
from watchwidget.services.timezone import current_reference_hour
from watchwidget.widgets.hour_header import HourHeader
from watchwidget.widgets.timeline_row import TimelineRow


class DesktopWidgetWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._scrubber = ScrubberState(current_reference_hour(), self)
        self._rows: list[TimelineRow] = []

        self.setWindowTitle("WatchWidget")
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowStaysOnBottomHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        self.setGeometry(WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMinimumSize(560, 210)

        self._build_ui()
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.refresh)
        self._timer.start(1000)

    def showEvent(self, event) -> None:  # noqa: N802 - Qt API
        super().showEvent(event)
        QTimer.singleShot(0, self.pin_to_desktop)

    def focusInEvent(self, event) -> None:  # noqa: N802 - Qt API
        super().focusInEvent(event)
        QTimer.singleShot(0, self.pin_to_desktop)

    def changeEvent(self, event: QEvent) -> None:  # noqa: N802 - Qt API
        super().changeEvent(event)
        if event.type() == QEvent.Type.ActivationChange and self.isActiveWindow():
            QTimer.singleShot(0, self.pin_to_desktop)

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802 - Qt API
        if event.key() == Qt.Key.Key_Escape:
            self.close()
            return
        super().keyPressEvent(event)

    def refresh(self) -> None:
        for row in self._rows:
            row.refresh()

    def pin_to_desktop(self) -> None:
        pin_to_desktop(int(self.winId()))

    def _build_ui(self) -> None:
        central = QWidget(self)
        central.setObjectName("root")

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)

        left_spacer = QWidget()
        left_spacer.setFixedWidth(LEFT_PANEL_WIDTH + 78)
        header_layout.addWidget(left_spacer)
        header_layout.addWidget(HourHeader(self), stretch=1)
        main_layout.addLayout(header_layout)

        for city in CITIES:
            row = TimelineRow(city=city, scrubber=self._scrubber, parent=self)
            self._rows.append(row)
            main_layout.addWidget(row)

        self.setCentralWidget(central)
        self._apply_stylesheet()

    def _apply_stylesheet(self) -> None:
        self.setStyleSheet(
            f"""
            QWidget#root {{
                background: {COLORS["window_bg"]};
                border: 1px solid {COLORS["border"]};
            }}
            """
            + TimelineRow.stylesheet()
        )


def ensure_single_app() -> QApplication:
    app = QApplication.instance()
    if app is not None:
        return app
    return QApplication([])
