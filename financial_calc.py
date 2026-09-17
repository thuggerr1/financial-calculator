import datetime
import calendar
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

class FinanceCalculator:
    def __init__(self, principal, rate_schedule):
        try:
            self.principal = float(principal)
            if self.principal < 0:
                raise ValueError("Початкова сума не може бути від'ємною.")
            
            self.rate_schedule = rate_schedule
        except ValueError as e:
            print(f"Помилка ініціалізації: {e}")
            raise

    def _calculate_days(self, start_date, end_date, method):
        try:
            if start_date > end_date:
                raise ValueError("Дата початку не може бути пізнішою за дату кінця.")
                
            if method in ['exact', 'commercial']:
                return (end_date - start_date).days
            elif method == 'ordinary':
                d1, m1, y1 = start_date.day, start_date.month, start_date.year
                d2, m2, y2 = end_date.day, end_date.month, end_date.year
                
                if d1 == 31: d1 = 30
                if d2 == 31: d2 = 30
                
                return 360 * (y2 - y1) + 30 * (m2 - m1) + (d2 - d1)
            else:
                raise ValueError(f"Невідомий метод нарахування: {method}")
        except Exception as e:
            print(f"Помилка розрахунку днів: {e}")
            raise

    def future_value(self, method='commercial'):
        try:
            total_interest = 0
            for period in self.rate_schedule:
                days = self._calculate_days(period['start'], period['end'], method)
                
                if method in ['ordinary', 'commercial']:
                    base = 360
                elif method == 'exact':
                    base = 366 if calendar.isleap(period['start'].year) else 365
                else:
                    raise ValueError(f"Невідомий метод нарахування: {method}")
                    
                total_interest += float(period['rate']) * (days / base)
                
            return self.principal * (1 + total_interest)
        except KeyError as e:
            print(f"FV: Відсутній обов'язковий ключ {e} у розкладі ставок.")
        except TypeError:
            print("FV: Неправильний тип даних для дат або ставок.")
        except Exception as e:
            print(f"Неочікувана помилка в future_value: {e}")

    def present_value(self, target_fv, method='commercial'):
        try:
            total_interest = 0
            for period in self.rate_schedule:
                days = self._calculate_days(period['start'], period['end'], method)
                
                if method in ['ordinary', 'commercial']:
                    base = 360
                elif method == 'exact':
                    base = 366 if calendar.isleap(period['start'].year) else 365
                else:
                    raise ValueError(f"Невідомий метод нарахування: {method}")
                    
                total_interest += float(period['rate']) * (days / base)
                
            return float(target_fv) / (1 + total_interest)
        except ZeroDivisionError:
            print("PV: Ділення на нуль (проблема з відсотковою ставкою).")
        except KeyError as e:
            print(f"PV: Відсутній обов'язковий ключ {e} у розкладі ставок.")
        except TypeError:
            print("PV: Неправильний тип даних.")
        except Exception as e:
            print(f"Неочікувана помилка в present_value: {e}")

    def accumulated_value(self):
        try:
            ordinary_value = self.future_value(method='ordinary')
            commercial_value = self.future_value(method='commercial')
            exact_value = self.future_value(method='exact')
            
            return ordinary_value, commercial_value, exact_value
        except Exception as e:
            print(f"Помилка у методі accumulated_value: {e}")

    def interest_rate(self):
        def get_average_rate(method):
            total_days = 0
            weighted_sum = 0
            
            for period in self.rate_schedule:
                days = self._calculate_days(period['start'], period['end'], method)
                total_days += days
                weighted_sum += float(period['rate']) * days
                
            return (weighted_sum / total_days) if total_days > 0 else 0

        try:
            ordinary_rate = get_average_rate('ordinary')
            commercial_rate = get_average_rate('commercial')
            exact_rate = get_average_rate('exact')
            
            return ordinary_rate, commercial_rate, exact_rate
        except KeyError as e:
            print(f"Помилка розрахунку ставки: Відсутній ключ {e}.")
        except Exception as e:
            print(f"Неочікувана помилка в interest_rate: {e}")

    def real_future_value(self, inflation_rate, method='commercial'):
        try:
            nominal_fv = self.future_value(method)
            total_n = 0
            for period in self.rate_schedule:
                days = self._calculate_days(period['start'], period['end'], method)
                if method in ['ordinary', 'commercial']:
                    base = 360
                elif method == 'exact':
                    base = 366 if calendar.isleap(period['start'].year) else 365
                else:
                    raise ValueError(f"Невідомий метод нарахування: {method}")
                
                n = days / base
                total_n += n
            real_fv = nominal_fv / ((1 + inflation_rate) ** total_n)
            return real_fv
        except Exception as e:
            print(f"Помилка у розрахунку майбутньої вартості з врахуванням інфляції: {e}")

    def plot_growth(self, inflation_rate, method='commercial'):
        try:
            x_days = [0]
            y_nominal = [self.principal]
            y_real = [self.principal]
            
            total_days = 0
            current_fv = self.principal
            total_n = 0
            for period in self.rate_schedule:
                days = self._calculate_days(period['start'], period['end'], method)
                total_days += days
                
                if method in ['ordinary', 'commercial']:
                    base = 360
                elif method == 'exact':
                    base = 366 if calendar.isleap(period['start'].year) else 365
                else:
                    raise ValueError(f"Невідомий метод нарахування: {method}")
                
                n = days / base
                total_n += n
                
                current_fv += self.principal * float(period['rate']) * n
                current_real = current_fv / ((1 + inflation_rate) ** total_n)

                x_days.append(total_days)
                y_nominal.append(current_fv)
                y_real.append(current_real)

            plt.plot(x_days, y_nominal, label='Номінальна вартість')
            plt.plot(x_days, y_real, label='З урахуванням інфляції')
            plt.xlabel('Дні')
            plt.ylabel('Вартість')
            plt.title('Зростання вартості з часом')
            plt.legend()
            plt.show()
        except Exception as e:
            print(f"Помилка у побудові графіку: {e}")


if __name__ == "__main__":
        my_schedule = [
        {'rate': 0.10, 'start': datetime.date(2026, 1, 1), 'end': datetime.date(2026, 6, 1)},
        {'rate': 0.12, 'start': datetime.date(2026, 6, 1), 'end': datetime.date(2026, 12, 31)}
    ]
        calc = FinanceCalculator(10000, my_schedule)        
        print(f"FV (звичайні, комерційні, точні): {calc.accumulated_value()}")
        print(f"Середні ставки: {calc.interest_rate()}")
        print(f"Реальна FV (інфляція 5%): {calc.real_future_value(0.05)}")
        print(f"Шукаємо PV (якщо FV = 11000): {calc.present_value(11000)}")
        calc.plot_growth(0.08)