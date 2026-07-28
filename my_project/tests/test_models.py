
import pytest
from datetime import datetime, date

from bank.models import BankAccount, InsufficientFundsError, Bank
from bank.transaction_utils import save_transactions, load_transactions
from bank.datetime_utils import transactions_today
from bank.transaction_analysis import summarize_transactions


def test_deposit():
    account = BankAccount("Farooq", 1000.0)

    account.deposit(500.0)

    assert account.get_balance() == 1500.0


def test_withdraw():
    account = BankAccount("Farooq", 1000.0)

    account.withdraw(300.0)

    assert account.get_balance() == 700.0


def test_withdraw_insufficient_funds():
    account = BankAccount("Farooq", 1000.0)

    with pytest.raises(InsufficientFundsError):
        account.withdraw(2000.0)


def test_transactions_today():
    transactions = [
        {
            "id": 1,
            "amount": 500,
            "timestamp": datetime.now(),
        },
        {
            "id": 2,
            "amount": 1000,
            "timestamp": datetime(2025, 1, 1),
        },
    ]

    result = transactions_today(transactions)

    assert len(result) == 1
    assert result[0]["id"] == 1


def test_summarize_transactions():
    transactions = [
        {"category": "deposit", "amount": 500},
        {"category": "deposit", "amount": 700},
        {"category": "withdrawal", "amount": 300},
    ]

    totals, amounts = summarize_transactions(transactions)

    assert totals["deposit"] == 2
    assert totals["withdrawal"] == 1

    assert amounts["deposit"] == [500, 700]
    assert amounts["withdrawal"] == [300]