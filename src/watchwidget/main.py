from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from watchwidget.desktop.window import DesktopWidgetWindow


def run() -> int:
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    window = DesktopWidgetWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(run())
