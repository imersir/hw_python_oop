import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.date.today()
        today_count = 0
        for record in self.records:
            if record.date == today:
                today_count += record.amount
        return today_count

    def get_week_stats(self):
        today = dt.date.today()
        delta = dt.timedelta(days=7)
        desired_date = today - delta
        week_count = 0
        for record in self.records:
            if today >= record.date > desired_date:
                week_count += record.amount
        return week_count


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        total_calories = self.limit - self.get_today_stats()
        if total_calories > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {total_calories} кКал')
        return f"Хватит есть!"


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0
    RUB_RATE = 1

    def get_today_cash_remained(self, currency):
        currencies = {
            'usd': ('USD', CashCalculator.USD_RATE),
            'eur': ('Euro', CashCalculator.EURO_RATE),
            'rub': ('руб', CashCalculator.RUB_RATE)
        }
        currency_title, currency_rate = currencies[currency]
        remainder = self.limit - self.get_today_stats()
        remainder_currency = round(remainder / currency_rate, 2)
        if remainder == 0:
            return "Денег нет, держись"
        if remainder_currency > 0:
            return f'На сегодня осталось {remainder_currency} {currency_title}'
        return (f'Денег нет, держись: твой долг - {abs(remainder_currency)} '
                f'{currency_title}')


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


if __name__ == '__main__':
    cash_calculator = CashCalculator(1000)
    cash_calculator.add_record(Record(amount=145, comment="кофе"))
    cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
    cash_calculator.add_record(
        Record(amount=3000, comment="бар в Танин др", date="08.11.2019"))
    print(cash_calculator.get_today_cash_remained("rub"))
