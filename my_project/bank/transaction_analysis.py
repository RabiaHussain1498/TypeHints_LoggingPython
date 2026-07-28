from collections import Counter, defaultdict


def summarize_transactions(
    transactions: list[dict],
) -> tuple[Counter, defaultdict]:
    category_totals = Counter()
    category_amounts = defaultdict(list)

    for transaction in transactions:
        category = transaction["category"]
        amount = transaction["amount"]

        category_totals[category] += 1
        category_amounts[category].append(amount)

    return category_totals, category_amounts