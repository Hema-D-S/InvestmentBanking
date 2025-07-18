class EmergencyFundCalculatorService:
    @staticmethod
    def calculate_recommended_fund(monthly_expenses: float, months: int = 6) -> float:
        """
        Calculate the recommended emergency fund size.
        :param monthly_expenses: User's average monthly expenses
        :param months: Number of months to cover (default: 6)
        :return: Recommended emergency fund amount
        """
        if monthly_expenses < 0 or months <= 0:
            raise ValueError("Monthly expenses and months must be positive numbers.")
        return round(monthly_expenses * months, 2)
