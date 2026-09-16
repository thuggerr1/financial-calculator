import datetime
import calendar
import matplotlib.pyplot as plt
import numpy as np

class FinanceCalculator:
    def __init__(self, principal, rate_schedule):
        self.principal = principal
        self.rate_schedule = rate_schedule

    def _calculate_days(self, start_date, end_date, method):
        if method in ['exact', 'commercial']:
            return (end_date - start_date).days
        elif method == 'ordinary':
            d1, m1, y1 = start_date.day, start_date.month, start_date.year
            d2, m2, y2 = end_date.day, end_date.month, end_date.year
            
            if d1 == 31: d1 = 30
            if d2 == 31: d2 = 30
            
            return 360 * (y2 - y1) + 30 * (m2 - m1) + (d2 - d1)

    def future_value(self, method='commercial'):
        total_interest = 0
        for period in self.rate_schedule:
            days = self._calculate_days(period['start'], period['end'], method)
            
            if method in ['ordinary', 'commercial']:
                base = 360
            elif method == 'exact':
                base = 366 if calendar.isleap(period['start'].year) else 365
                
            total_interest += period['rate'] * (days / base)
            
        return self.principal * (1 + total_interest)

    def present_value(self, target_fv, method='commercial'):
        total_interest = 0
        for period in self.rate_schedule:
            days = self._calculate_days(period['start'], period['end'], method)
            
            if method in ['ordinary', 'commercial']:
                base = 360
            elif method == 'exact':
                base = 366 if calendar.isleap(period['start'].year) else 365
                
            total_interest += period['rate'] * (days / base)
            
        return target_fv / (1 + total_interest)

    def accumulated_value(self):
        ordinary_value = self.future_value(method='ordinary')
        commercial_value = self.future_value(method='commercial')
        exact_value = self.future_value(method='exact')
        
        return ordinary_value, commercial_value, exact_value

    def interest_rate(self):
        def get_average_rate(method):
            total_days = 0
            weighted_sum = 0
            
            for period in self.rate_schedule:
                days = self._calculate_days(period['start'], period['end'], method)
                total_days += days
                weighted_sum += period['rate'] * days
                
            return (weighted_sum / total_days) if total_days > 0 else 0

        ordinary_rate = get_average_rate('ordinary')
        commercial_rate = get_average_rate('commercial')
        exact_rate = get_average_rate('exact')
        
        return ordinary_rate, commercial_rate, exact_rate

    