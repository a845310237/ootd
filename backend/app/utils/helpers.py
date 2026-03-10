"""Template helper functions for Jinja2 templates."""
from datetime import datetime
from typing import Any
import json


def format_date(value: datetime, format_str: str = "%Y-%m-%d") -> str:
    """
    Format a datetime object to a string.

    Args:
        value: Datetime object to format
        format_str: Format string (default: "%Y-%m-%d")

    Returns:
        str: Formatted date string
    """
    if value is None:
        return ""
    return value.strftime(format_str)


def format_datetime(value: datetime) -> str:
    """
    Format a datetime object to a datetime string.

    Args:
        value: Datetime object to format

    Returns:
        str: Formatted datetime string
    """
    return format_date(value, "%Y-%m-%d %H:%M:%S")


def json_parse(value: str) -> Any:
    """
    Parse a JSON string into a Python object.

    Args:
        value: JSON string to parse

    Returns:
        Any: Parsed Python object (list, dict, etc.)
    """
    if value is None:
        return []
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return []


def json_dumps(value: Any) -> str:
    """
    Convert a Python object to a JSON string.

    Args:
        value: Python object to convert

    Returns:
        str: JSON string
    """
    try:
        return json.dumps(value, ensure_ascii=False)
    except (TypeError, ValueError):
        return "[]"


def truncate(text: str, length: int = 50, suffix: str = "...") -> str:
    """
    Truncate text to a specified length.

    Args:
        text: Text to truncate
        length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        str: Truncated text
    """
    if text is None:
        return ""
    if len(text) <= length:
        return text
    return text[:length] + suffix


def join_list(items: list, separator: str = ", ") -> str:
    """
    Join a list of items into a string.

    Args:
        items: List of items to join
        separator: Separator string

    Returns:
        str: Joined string
    """
    if items is None:
        return ""
    return separator.join(str(item) for item in items)


def get_first_item(items: list, default: Any = None) -> Any:
    """
    Get the first item from a list or return default.

    Args:
        items: List to get first item from
        default: Default value if list is empty

    Returns:
        Any: First item or default value
    """
    if items and len(items) > 0:
        return items[0]
    return default


def is_list(value: Any) -> bool:
    """
    Check if a value is a list.

    Args:
        value: Value to check

    Returns:
        bool: True if value is a list
    """
    return isinstance(value, list)


def is_dict(value: Any) -> bool:
    """
    Check if a value is a dict.

    Args:
        value: Value to check

    Returns:
        bool: True if value is a dict
    """
    return isinstance(value, dict)


def get_attr(obj: Any, attr: str, default: Any = None) -> Any:
    """
    Get an attribute from an object safely.

    Args:
        obj: Object to get attribute from
        attr: Attribute name
        default: Default value if attribute doesn't exist

    Returns:
        Any: Attribute value or default
    """
    return getattr(obj, attr, default)


def nl2br(text: str) -> str:
    """
    Convert newlines to <br> tags.

    Args:
        text: Text to convert

    Returns:
        str: Text with <br> tags
    """
    if text is None:
        return ""
    return text.replace("\n", "<br>")


def static_url(path: str) -> str:
    """
    Generate a static file URL.

    Args:
        path: Path to static file

    Returns:
        str: Static file URL
    """
    return f"/static/{path}"


# Register all helpers
def register_helpers(env):
    """
    Register custom helpers with Jinja2 environment.

    Args:
        env: Jinja2 environment
    """
    env.filters['format_date'] = format_date
    env.filters['format_datetime'] = format_datetime
    env.filters['json_parse'] = json_parse
    env.filters['json_dumps'] = json_dumps
    env.filters['truncate'] = truncate
    env.filters['join_list'] = join_list
    env.filters['nl2br'] = nl2br

    env.globals['get_first_item'] = get_first_item
    env.globals['is_list'] = is_list
    env.globals['is_dict'] = is_dict
    env.globals['get_attr'] = get_attr
    env.globals['static_url'] = static_url
