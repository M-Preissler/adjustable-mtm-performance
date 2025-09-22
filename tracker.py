"""
Tracker module for the Office Assistant prototype.

This module provides a simple interface to log which window is
active over a period of time. It uses the pygetwindow library
to determine the active window title. The primary function,
track_activity, returns a list of dictionaries capturing the
timestamp and window title at regular intervals. Consumers can
persist this list or further process it as needed.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List
import pygetwindow


def track_activity(duration: int, interval: float = 1.0) -> List[Dict[str, Any]]:
    """
    Track the active window title over a period of time.

    Parameters
    ----------
    duration: int
        Duration to track in seconds.
    interval: float, optional
        Number of seconds between checks. Defaults to 1.0.

    Returns
    -------
    List[Dict[str, Any]]
        A list of records containing timestamp and window title.
    """
    records: List[Dict[str, Any]] = []
    end_time = time.time() + duration
    while time.time() < end_time:
        # Query the currently active window. Some systems may return None.
        win = pygetwindow.getActiveWindow()
        title = win.title if win else "Unknown"
        records.append({
            "timestamp": time.time(),
            "title": title,
        })
        time.sleep(interval)
    return records