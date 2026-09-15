import datetime
import calendar
import matplotlib.pyplot as plt
import numpy as np

class FinanceCalculator:
    def __init__(self, principal, end_date, annual_rate, start_date=None):
        self.principal = principal
        self.end_date = end_date
        self.annual_rate = annual_rate
        if start_date is None: 
            self.start_date = datetime.datetime.today()
        else:
            self.start_date = start_date

    def future_value(self, years):
        return self.principal * (1 + self.annual_rate * years)

    def present_value(self, future_value, years):
        return future_value / (1 + self.annual_rate * years)

    def accumulated_value(self):
        actual_days = (self.end_date - self.start_date).days
        ordinary_value = self.future_value(actual_days / 360)        
        commercial_value = self.future_value(actual_days / 365)
        if calendar.isleap(self.start_date.year):
            days_in_year = 366
        else:
            days_in_year = 365
        exact_value = self.future_value(actual_days / days_in_year)
        return ordinary_value, commercial_value, exact_value

    def interest_rate(self):
        