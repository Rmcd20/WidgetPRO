from __future__ import annotations

import sys

if sys.platform == "win32":
    import win32con
    import win32gui
else:  # pragma: no cover - the app targets Windows, but imports should remain safe.
    win32con = None
    win32gui = None


def pin_to_desktop(hwnd: int) -> None:
    if sys.platform != "win32" or win32con is None or win32gui is None:
        return

    ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    ex_style |= win32con.WS_EX_TOOLWINDOW
    ex_style &= ~win32con.WS_EX_APPWINDOW
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style)

    win32gui.SetWindowPos(
        hwnd,
        win32con.HWND_BOTTOM,
        0,
        0,
        0,
        0,
        win32con.SWP_NOMOVE
        | win32con.SWP_NOSIZE
        | win32con.SWP_NOACTIVATE
        | win32con.SWP_SHOWWINDOW,
    )
