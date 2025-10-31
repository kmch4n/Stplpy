"""
Utility functions for Stplpy library.
"""
from datetime import datetime, timezone
from typing import Dict, Any, List


def format_study_duration(seconds: int) -> str:
    """
    Format study duration in seconds to human-readable format.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string (e.g., "1h 30m")
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60

    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if remaining_seconds > 0 or not parts:
        parts.append(f"{remaining_seconds}s")

    return " ".join(parts)


def parse_iso_datetime(iso_string: str) -> datetime:
    """
    Parse ISO 8601 datetime string.

    Args:
        iso_string: ISO 8601 formatted datetime string

    Returns:
        datetime object
    """
    return datetime.fromisoformat(iso_string.replace('Z', '+00:00'))


def get_current_utc_time() -> str:
    """
    Get current UTC time in ISO 8601 format.

    Returns:
        Current UTC time as ISO string
    """
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def extract_user_ids(timeline_feeds: List[Dict[str, Any]]) -> List[str]:
    """
    Extract unique user IDs from timeline feeds.

    Args:
        timeline_feeds: List of timeline feed items

    Returns:
        List of unique user IDs
    """
    user_ids = set()
    for feed in timeline_feeds:
        if "user_id" in feed:
            user_ids.add(feed["user_id"])
    return list(user_ids)


def calculate_total_study_time(records: List[Dict[str, Any]]) -> int:
    """
    Calculate total study time from study records.

    Args:
        records: List of study records

    Returns:
        Total duration in seconds
    """
    total = 0
    for record in records:
        if "duration" in record:
            total += record["duration"]
    return total


def group_by_date(records: List[Dict[str, Any]], date_field: str = "record_datetime") -> Dict[str, List[Dict[str, Any]]]:
    """
    Group records by date.

    Args:
        records: List of records
        date_field: Field name containing the date

    Returns:
        Dictionary mapping dates to lists of records
    """
    grouped = {}
    for record in records:
        if date_field in record:
            date_str = record[date_field].split('T')[0]  # Extract date part
            if date_str not in grouped:
                grouped[date_str] = []
            grouped[date_str].append(record)
    return grouped
