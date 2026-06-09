from __future__ import annotations

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from watchwidget.config import DAY_END, DAY_START, REF_TZ
from watchwidget.models import City


def reference_day_start(now: datetime | None = None) -> datetime:
    ref_now = now.astimezone(REF_TZ) if now else datetime.now(REF_TZ)
    return ref_now.replace(hour=0, minute=0, second=0, microsecond=0)


def instant_for_reference_hour(hour: int, now: datetime | None = None) -> datetime:
    return reference_day_start(now) + timedelta(hours=hour)


def local_datetime_for_reference_hour(
    city: City,
    hour: int,
    now: datetime | None = None,
) -> datetime:
    return instant_for_reference_hour(hour, now).astimezone(city.timezone)


def hour_is_daylight(city: City, reference_hour: int, now: datetime | None = None) -> bool:
    local = local_datetime_for_reference_hour(city, reference_hour, now)
    return DAY_START <= local.hour < DAY_END


def format_clock(dt: datetime) -> str:
    return f"{dt.hour:02d}:{dt.minute:02d}"


def format_hour_label(reference_hour: int) -> str:
    return f"{reference_hour % 24:02d}"


def current_reference_hour() -> int:
    return datetime.now(REF_TZ).hour


def timezone_abbreviation(city: City) -> str:
    return datetime.now(city.timezone).tzname() or ""


def offset_from_reference(city: City) -> str:
    now_ref = datetime.now(REF_TZ)
    ref_offset = now_ref.utcoffset()
    city_offset = now_ref.astimezone(city.timezone).utcoffset()
    if ref_offset is None or city_offset is None:
        return "±0"

    diff_hours = int((city_offset - ref_offset).total_seconds() // 3600)
    if diff_hours == 0:
        return "±0"
    sign = "+" if diff_hours > 0 else ""
    return f"{sign}{diff_hours}"


def now_for_city(city: City) -> datetime:
    return datetime.now(city.timezone)
