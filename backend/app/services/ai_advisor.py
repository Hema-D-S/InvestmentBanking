from typing import Dict

class AIAdvisorService:
    @staticmethod
    def generate_advice(user_profile: Dict, financial_data: Dict) -> str:
        # In production, integrate with an AI/ML model or external API
        # Here, we mock the advice for demonstration
        if financial_data.get("savings", 0) < 1000:
            return "Consider increasing your monthly savings to build a stronger financial cushion."
        if financial_data.get("debt", 0) > 5000:
            return "Focus on paying down high-interest debt to improve your financial health."
        return "Your finances look healthy! Keep tracking your goals and investments."
