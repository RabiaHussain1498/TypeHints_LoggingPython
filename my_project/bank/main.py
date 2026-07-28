from bank.models import (Bank, BankAccount, InsufficientFundsError,logger,)
from bank.transaction_utils import (save_transactions,load_transactions,)
from datetime import datetime, date
from bank.datetime_utils import transactions_today
from bank.transaction_analysis import summarize_transactions


def run_demo() -> None:
    # Create an account and perform a successful deposit
    account = BankAccount("Farooq", 1500.0)
    account.deposit(2500.0)
    logger.info("Balance after deposit: %.2f", account.get_balance())

    # Create a bank and open an account
    bank = Bank()
    bank.open_account("Farooq", 1000.0)

 
    logger.info(
        "Total bank balance: %.2f",
        bank.total_balance(),
)
    
    # Demonstrate that type hints are not enforced at runtime
    try:
        account.deposit("fifty")  # type: ignore[arg-type]
    except TypeError as exc:
        logger.warning(
            "Python executed deposit('fifty'), then raised a runtime TypeError: %s",
            exc,
        )

    # Demonstrate custom exception
    try:
        account.withdraw(10000.0)
    except InsufficientFundsError:
        logger.error(
            "InsufficientFundsError raised for account owner: %s",
            account.owner,
        )

    logger.info("Final balance: %.2f", account.get_balance())
    

    transactions = [
    {"id": 1, "amount": 500.0, "category": "withdrawal"},
    {"id": 2, "amount": 1200.0, "category": "deposit"},
]
    save_transactions(
    "data/transactions.json",
    transactions,
      )

    logger.info("Transactions saved successfully")

    loaded = load_transactions(
      "data/transactions.json",
     )

    logger.info("Loaded transactions: %s", loaded)


    save_transactions(
    "data/transactions.json",
    transactions,
)


    today_transactions = transactions_today(loaded)

    logger.info("Today's transactions: %s", today_transactions)

    transactions = [
    {
        "category": "withdrawal",
        "amount": 1000,
    },
    {
        "category": "withdrawal",
        "amount": 2500,
    },
    {
        "category": "deposit",
        "amount": 500,
    },
]

    totals, amounts_by_category = summarize_transactions(
      transactions
     )

    logger.info(
     "Transaction counts by category: %s",
     totals,
    )

    logger.info(
     "Transaction amounts by category: %s",
     dict(amounts_by_category),
     )


if __name__ == "__main__":
    run_demo()