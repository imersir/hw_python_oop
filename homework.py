import datetime as dt


class Calculator:
    def __init__(self, limit: object):
        self.limit = limit
        self.records = []

    def add_record(self, record: object):
        """Добавляет новую запись в records."""
        self.records.append(record)

    def get_today_stats(self):
        """Сколько калорий съедено сегодня."""
        today = dt.date.today()
        today_list = []
        for record in self.records:
            if record.date == today:
                today_list.append(record.amount)
        return sum(today_list)

    def get_week_stats(self):
        """Сколько денег потрачено за последние 7 дней."""
        today = dt.date.today()
        delta = dt.timedelta(days=7)
        desired_date = today - delta
        week_list = []
        for record in self.records:
            if today >= record.date > desired_date:
                week_list.append(record.amount)
        return sum(week_list)


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        """Сколько калорий можно(нужно) получить сегодня."""
        calories_remained = self.limit - self.get_today_stats()
        if calories_remained > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {calories_remained} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 60.0  # КОНСТАНТЫ всегда заглавными буквами
    EURO_RATE = 70.0  # КОНСТАНТЫ всегда заглавными буквами
    RUB_RATE = 1  # КОНСТАНТЫ всегда заглавными буквами

    def get_today_cash_remained(self, currency):
        """Сколько денег можно потратить сегодня в разных валютах."""
        currencies = {'usd': ('USD', CashCalculator.USD_RATE),
                      'eur': ('Euro', CashCalculator.EURO_RATE),
                      'rub': ('руб', CashCalculator.RUB_RATE)}
        currency_title, currency_rate = currencies[currency]
        remainder = self.limit - self.get_today_stats()
        remainder_currency = round(remainder / currency_rate, 2)
        if remainder == 0:
            return "Денег нет, держись"
        if currency not in currencies:
            return f'Валюта {currency} отсутствует'
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
