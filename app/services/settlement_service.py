import logging
import os
from payment_checker import PaymentCheckerNew

# wrapper to decouple direct import and to maintain instance/balance state
class SettlementService:
    def __init__(self):
        # PaymentCheckerNew expects env vars; ensure env loaded beforehand
        self.checker = PaymentCheckerNew()

    def check_payment(self, amount: int):
        """
        Returns dict in the same format used in your original checker:
        {'success': True/False, 'data': {...}} or {'success': False, 'error': '...'}
        """
        return self.checker.check_payment_status(amount)

settlement_service = SettlementService()
