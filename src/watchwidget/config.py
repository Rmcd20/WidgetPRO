from __future__ import annotations

from zoneinfo import ZoneInfo

from watchwidget.models import City

REF_TZ = ZoneInfo("Europe/Lisbon")
DAY_START = 7
DAY_END = 19
HOUR_COUNT = 24

CITIES: tuple[City, ...] = (
    City("Portugal", REF_TZ),
    City("Madrid", ZoneInfo("Europe/Madrid")),
    City("Argentina", ZoneInfo("America/Argentina/Buenos_Aires")),
    City("Colombia", ZoneInfo("America/Bogota")),
)

WINDOW_WIDTH = 760
WINDOW_HEIGHT = 260
WINDOW_X = 40
WINDOW_Y = 40

LEFT_PANEL_WIDTH = 185
ROW_HEIGHT = 44
HEADER_HEIGHT = 32
TIMELINE_MIN_WIDTH = 520

COLORS = {
    "window_bg": "#f3f3f3",
    "panel_bg": "#ffffff",
    "text": "#202020",
    "muted": "#767676",
    "border": "#d7d7d7",
    "day": "#d9edf6",
    "night": "#79a6cf",
    "hour_text": "#244f6c",
    "hour_text_night": "#f7fbff",
    "header_text": "#385f78",
    "scrubber": "#285d8f",
    "scrubber_fill": "#285d8f55",
}
