import os
import pickle
from datetime import datetime


def list_expenses(category: str = None, start_date: str = None, end_date: str = None):
    """
    Lists saved expenses, with optional filters for category and/or a date range.

    For the model: Use this tool to show the user their past expenses. All
    parameters are optional and can be combined. If filtering by a date range,
    ensure both start and end dates are in 'YYYY-MM-DD' format.

    Args:
        category (str, optional): The category to filter expenses by.
        start_date (str, optional): The start of the date range (YYYY-MM-DD).
        end_date (str, optional): The end of the date range (YYYY-MM-DD).

    Returns:
        list: A list of expense dictionaries that match the criteria. You should
              parse this list and present it to the user in a readable format,
              such as a Markdown table.

    Raises:
        ValueError: If any provided date strings are not in YYYY-MM-DD format.
    """
    if start_date:
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                f"Invalid start_date: {start_date}. Date must be in YYYY-MM-DD format."
            )
    if end_date:
        try:
            datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                f"Invalid end_date: {end_date}. Date must be in YYYY-MM-DD format."
            )

    filepath = os.path.expanduser("~/data/expenses.pkl")
    try:
        with open(filepath, "rb") as f:
            expenses = pickle.load(f)
    except (FileNotFoundError, EOFError):
        return []

    filtered = [
        exp
        for exp in expenses
        if (category is None or exp["category"].lower() == category.lower())
        and (start_date is None or exp["date"] >= start_date)
        and (end_date is None or exp["date"] <= end_date)
    ]
    return filtered
