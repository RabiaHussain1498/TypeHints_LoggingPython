from pathlib import Path
from datetime import datetime,date
import json


def save_transactions(
    path: str | Path,
    transactions: list[dict],
) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            transactions,
            file,
            indent=2,
            default=str,
        )


def load_transactions(
    path: str | Path,
) -> list[dict]:
    path = Path(path)

    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    for transaction in data:
        if "timestamp" in transaction:
            transaction["timestamp"] = datetime.fromisoformat(
                transaction["timestamp"]
            )

    return data