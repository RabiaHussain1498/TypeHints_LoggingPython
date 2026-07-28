

from datetime import datetime, date

def transactions_today(transactions):
    today = date.today()
    return [
        t for t in transactions
        if isinstance(t.get("timestamp"), datetime)
        and t["timestamp"].date() == today
    ]