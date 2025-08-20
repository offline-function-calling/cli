from datetime import datetime


def get_time():
    """
    Returns the current date and time for the local machine's timezone.

    This tool is for when the user asks for the current date, time, or day.

    For the model: It is also critically important for providing a default
    date for other tools, like 'record_expense', when the user says "today"
    or "now". The output is a structured JSON object. You must parse this
    object to extract and present the specific information the user requested
    (e.g., just the time, or the full date).

    Args:
        None

    Returns:
        dict: A dictionary containing the formatted date and time parts, like
              the year, month, day, hour, minute, second, and day name.
    """
    now = datetime.now()
    return {
        "iso_format": now.isoformat(),
        "pretty_format": now.strftime("%A, %B %d, %Y - %I:%M:%S %p"),
        "year": now.year,
        "month": now.month,
        "day": now.day,
        "hour": now.hour,
        "minute": now.minute,
        "second": now.second,
        "weekday": now.strftime("%A"),
    }
