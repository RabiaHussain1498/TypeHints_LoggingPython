import logging
from pathlib import Path

log_file = Path("logs") / "bank_account.log"
log_file.parent.mkdir(exist_ok=True)
logger = logging.getLogger("bank_account")
logger.setLevel(logging.INFO)

if not logger.handlers:
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.propagate = False


class InsufficientFundsError(Exception):
    """Raised when the account balance is insufficient."""


class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0) -> None:
        self.owner: str = owner
        self.balance: float = balance

    def deposit(self, amount: float) -> None:
        self.balance += amount
        logger.info("Deposit of %.2f received for %s", amount, self.owner)

    def withdraw(self, amount: float) -> None:
        if amount > self.balance:
            logger.warning(
                "Withdrawal failed for %s: requested %.2f, available %.2f",
                self.owner,
                amount,
                self.balance,
            )
            raise InsufficientFundsError("Not enough money in the account")

        self.balance -= amount
        logger.info("Withdrawal of %.2f processed for %s", amount, self.owner)

    def get_balance(self) -> float:
        return self.balance


class Bank:
    def __init__(self) -> None:
        self.accounts: dict[str, BankAccount] = {}

    def open_account(self, owner: str, initial_balance: float = 0.0) -> BankAccount:
        account = BankAccount(owner, initial_balance)
        self.accounts[owner] = account
        return account

    def transfer(self, from_owner: str, to_owner: str, amount: float) -> None:
        sender = self.accounts[from_owner]
        receiver = self.accounts[to_owner]
        sender.withdraw(amount)
        receiver.deposit(amount)

    def total_balance(self) -> float:
        return sum(account.get_balance() for account in self.accounts.values())
