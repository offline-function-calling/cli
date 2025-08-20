import os, pickle
from datetime import datetime


def record_expense(category: str, amount: float, date: str, description: str = ""):
    """
    Records a new expense to a local file with a category, amount, and date.

    For the model: Use this tool to save a user's expense. You must extract a
    category, an amount, and a date. Always format dates as 'YYYY-MM-DD'. If
    the user says "today" or does not provide a date, you MUST use the
    'get_current_datetime' tool first to find today's date, and then use that
    resolved date when calling this tool.

    Args:
        category (str): The category of the expense (e.g., 'Food', 'Transport').
        amount (float): The monetary value of the expense.
        date (str): The date of the expense in YYYY-MM-DD format.
        description (str, optional): An optional description of the expense.

    Returns:
        str: A simple confirmation string upon success.

    Raises:
        ValueError: If the provided date string is not in YYYY-MM-DD format.
    """
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Date must be in YYYY-MM-DD format.")

    data_dir = os.path.expanduser("~/data")
    os.makedirs(data_dir, exist_ok=True)
    filepath = os.path.join(data_dir, "expenses.pkl")

    expenses = []
    if os.path.exists(filepath):
        try:
            with open(filepath, "rb") as f:
                expenses = pickle.load(f)
        except Exception:
            expenses = []

    expenses.append(
        {
            "category": category,
            "amount": amount,
            "date": date,
            "description": description,
        }
    )
    with open(filepath, "wb") as f:
        pickle.dump(expenses, f)

    return f"Successfully recorded expense: {amount} in {category} on {date}."
