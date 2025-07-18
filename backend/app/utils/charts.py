import matplotlib.pyplot as plt
import io
from typing import List, Dict

def generate_expense_bar_chart(expenses: List[Dict[str, float]]) -> bytes:
    """
    Generate a bar chart for monthly expenses.
    :param expenses: List of dicts with 'month' and 'amount' keys
    :return: PNG image bytes
    """
    months = [item['month'] for item in expenses]
    amounts = [item['amount'] for item in expenses]
    plt.figure(figsize=(8, 4))
    plt.bar(months, amounts, color='skyblue')
    plt.xlabel('Month')
    plt.ylabel('Amount ($)')
    plt.title('Monthly Expenses')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.getvalue()
