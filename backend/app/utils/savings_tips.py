import random
from typing import Dict

def get_random_savings_tip() -> str:
    tips = [
        "Set up automatic transfers to your savings account.",
        "Track your expenses to find hidden savings.",
        "Review subscriptions and cancel unused ones.",
        "Set specific, measurable savings goals.",
        "Use cash-back and rewards programs wisely.",
        "Cook at home more often to save on dining out.",
        "Review your budget monthly and adjust as needed."
    ]
    return random.choice(tips)

def generate_savings_tip(user_profile: Dict) -> str:
    # Example: Dynamic tip based on user data
    if user_profile.get("savings", 0) < 500:
        return "Try to save at least 10% of your monthly income."
    if user_profile.get("debt", 0) > 2000:
        return "Focus on paying down high-interest debt before increasing savings."
    return get_random_savings_tip()
