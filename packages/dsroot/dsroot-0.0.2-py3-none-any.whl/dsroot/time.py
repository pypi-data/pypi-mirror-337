from __future__ import annotations

import warnings
from datetime import datetime, timedelta
from functools import partial
from typing import Any
from zoneinfo import ZoneInfo

from tzlocal import get_localzone

from dsroot.singleton import Singleton


class TimeZoneManager(metaclass=Singleton):
    """Singleton class for managing the local timezone."""

    _warning_shown = False

    def __init__(self):
        self._timezone = self._detect_timezone()

    def _detect_timezone(self) -> ZoneInfo:
        try:  # Try to get the local timezone
            local_tz_str = str(get_localzone())
            return ZoneInfo(local_tz_str)
        except Exception:
            # If detection fails, show a warning on the first check only
            if not TimeZoneManager._warning_shown:
                warn_text = "Could not detect local timezone, defaulting to America/New_York"
                warnings.warn(warn_text, UserWarning, stacklevel=2)
                TimeZoneManager._warning_shown = True

            return ZoneInfo("America/New_York")

    def get_timezone(self) -> ZoneInfo:
        """Get the local timezone."""
        return self._timezone


# Create TZ object for easy access
TZ = TimeZoneManager().get_timezone()


class Time:
    """Time parser and formatter for various formats and relative time interpretations."""

    @staticmethod
    def get_pretty_time(time: datetime | timedelta, **kwargs: Any) -> str:
        """Given a timestamp, return a pretty string representation of the time.

        Args:
            time: The timestamp to convert.
            **kwargs: Additional keyword arguments to pass to the formatting function.
                - capitalize: If True, the first letter of the string will be capitalized.
                - time_only: If True, only the time will be returned, not the date.
                - weekday: If True, the weekday will be included in the date format.
                - compact: If True, use a more compact format for dates within 7 days.
        """
        if isinstance(time, datetime):
            return Time._format_datetime(time, **kwargs)
        return Time._format_timedelta(time)

    @staticmethod
    def _format_datetime(
        time: datetime,
        capitalize: bool = False,
        time_only: bool = False,
        weekday: bool = False,
        compact: bool = False,
    ) -> str:
        now = datetime.now(tz=TZ)

        if time_only:
            return time.strftime("%-I:%M %p")

        days_difference = (time.date() - now.date()).days

        if days_difference == 0:
            result = f"today at {time.strftime('%-I:%M %p')}"
        elif days_difference == -1:
            result = f"yesterday at {time.strftime('%-I:%M %p')}"
        elif days_difference == 1:
            result = f"tomorrow at {time.strftime('%-I:%M %p')}"
        elif compact and 1 < abs(days_difference) <= 7:
            result = time.strftime("%A at %-I:%M %p")
        else:
            result = time.strftime("%A, %B %d") if weekday or compact else time.strftime("%B %d")
            if abs(days_difference) > 365:
                result += time.strftime(", %Y")
            result += f" at {time.strftime('%-I:%M %p')}"

        return result.capitalize() if capitalize else result

    @staticmethod
    def _format_timedelta(time: timedelta) -> str:
        total_seconds = int(time.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours}h {minutes}m {seconds}s"

    @staticmethod
    def ensure_tz(dt: datetime) -> datetime:
        """Ensure datetime has the correct timezone."""
        if dt.tzinfo is None:
            return dt.replace(tzinfo=TZ)
        return dt.astimezone(TZ)


# Partial functions for common use cases
get_pretty_time = partial(Time.get_pretty_time)
get_capitalized_time = partial(Time.get_pretty_time, capitalize=True)
get_time_only = partial(Time.get_pretty_time, time_only=True)
get_weekday_time = partial(Time.get_pretty_time, weekday=True)
