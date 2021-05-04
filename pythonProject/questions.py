from weather import Manager
from termcolor import cprint


class Questions:

    def __init__(self):
        self.QUESTIONS = ["Добавить прогнозы за диапазон дат в базу данных?\n",
                          "Получить прогнозы за диапазон дат из базы?\n",
                          "Создать открытки из прогнозов?\n",
                          "Вывести прогнозы на консоль?\n"]
        self.TRUE_ANSWERS = ['Прогнозы добавлены', 'Прогнозы получены', 'Открытки созданы']
        self.FALSE_ANSWERS = ['Прогнозы из базы не получены, тк вы ничего не добавили в базу']
        self.DEFAULT_ANSWER = 'Введено неверное значение.'
        self.manager = Manager(date_range=None)
        self.forecast, self.forecast_from_db = None, None

    def first_question(self):
        """Загружает прогноз за последнюю неделю
        Возвращает новый прогноз и диапазон дат по желанию позьзователя"""
        past_week_forecasts = self.manager.make_weather_week_ago()
        while True:
            cprint('Прогнозы за прошедшую неделю загружены. ', color='green')
            cprint('Хотите получить прогнозы за другой диапазон дат?\nВведите "да" или "нет"', color='yellow')
            try_input = input()
            if try_input.lower() == 'да':
                while True:
                    cprint('Введите диапазон дат, на который вы хотите получить прогноз.'
                           ' Диапазон должен быть в формате дд.мм.гггг-дд.мм.гггг', color='yellow')
                    self.manager.date_range = input()
                    if not self.manager.check_date():
                        self.forecast = self.manager.parse_forecast()
                        return self.forecast, self.manager.date_range
                    else:
                        cprint(self.manager.check_date(), color='red')
            elif try_input.lower() == 'нет':
                self.forecast = past_week_forecasts
                return self.forecast, None
            else:
                cprint(self.DEFAULT_ANSWER, color='red')

    def asking(self):
        """Функция последовательно опрашивает пользователя и при ответе "да" - совершает действие"""
        forecast, date_range = self.first_question()
        for number, question in enumerate(self.QUESTIONS):
            while True:
                cprint(f'{question}Ответьте "да" или "нет"', color='green')
                answer = input().lower()
                if answer == 'да':
                    text = self.action(number, date_range)
                    cprint(text, color='yellow')
                    break
                elif answer == 'нет':
                    break
                else:
                    cprint(self.DEFAULT_ANSWER, color='red')

    def action(self, number, date_range=None):
        """Функция принимает на вход число, в зависимости от которого будет совершаться определенное действие"""
        if number == 0:
            self.manager.write_data_to_db(self.forecast)
            return self.TRUE_ANSWERS[0]
        elif number == 1:
            try:
                self.forecast = self.manager.get_data_from_db(date_range)
                return self.TRUE_ANSWERS[1]
            except Exception:
                return self.FALSE_ANSWERS[0]
        elif number == 2:
            self.manager.make_postcards(self.forecast)
            return self.TRUE_ANSWERS[2]
        elif number == 3:
            print_forecast = str()
            for forecast in self.forecast:
                for item, value in forecast.items():
                    print_forecast += f'{item}: {value}; '
                print_forecast += '\n'
            return print_forecast
