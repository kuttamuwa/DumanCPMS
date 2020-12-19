from django.test import TestCase

import pandas as pd

# Create your tests here.
from risk_analysis.models import DataSetModel
from risk_analysis.usermodel import UserAdaptor


class CreateRiskDatasetOne(TestCase):
    @classmethod
    def create(cls):
        customer = UserAdaptor.dummy_creator.create()
        rd = DataSetModel.objects.get_or_create(
            customer=customer,
            limit=1000000,
            warrant_state=False,
            warrant_amount=None,
            maturity=150,
            payment_frequency=None,
            maturity_exceed_avg=20000,
            avg_order_amount_last_three_months=690000,
            avg_order_amount_last_twelve_months=521141,
            last_3_months_aberration=None,
            last_month_payback_perc=None,
            last_twelve_months_payback_perc=3,
            last_three_months_payback_comparison=None,
            avg_last_three_months_payback_perc=None,
            avg_delay_time=15,
            avg_delay_balance=20000,
            period_day=352,
            period_velocity=1.0,
            risk_excluded_warrant_balance=509.429,
            balance=509.429,
            profit=100000,
            profit_percent=0.03,
            total_risk_including_cheque=509429,
            last_12_months_total_endorsement=3648000,
        )
        return rd[0]
