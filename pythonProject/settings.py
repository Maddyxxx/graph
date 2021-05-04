TOKEN = '1603522227:AAHSP42EU6b1t4QmDX4obkJAmiG_3JMYhqE'

INTENTS = [
    {
        "name": "Приветствие",
        "tokens": ("привет", "/start"),
        "scenario": None,
        "answer": "\tПривет!.\n"
                  "\tДля того, чтобы получить билет или прогноз, пройдите все шаги сценария\n"
                  "\n\tБот умеет распознавать команды на естественном языке\n"
                  "\tДоступны следующие команды:"
                  "\nНапиши /ticket чтобы получить билет или /forecast чтобы получить проноз погоды"
                  "\n/help - выводит справку о работе бота и доступные команды"
    },
    {
        "name": "Помощь",
        "tokens": ("/help", "помощь", "что ты умеешь?"),
        "scenario": None,
        "answer": "Доступны следующие функции:"
                  "\n/ticket - запускает сценарий заказа билетов"
                  "\n/forecast - запускает сценарий получения прогноза"
                  "\n/return или 'Назад' - возвращает на шаг назад"
    },
    {
        "name": "Заказ билетов",
        "tokens": "/ticket",
        "scenario": "make a ticket",
        "answer": None
    },
    {
        "name": "Получить прогноз",
        "tokens": "/forecast",
        "scenario": "forecast",
        "answer": None
    },
]

SCENARIOS = {
    "make a ticket": {
        "first_step": "step_1",
        "steps": {
            "step_1": {
                "text": "Введите город отправления",
                "failure_text": "{error}",
                "handler": "handle_departure_city",
                "next_step": "step_2",
                "prev_step": 'step_1'
            },
            "step_2": {
                "text": "Введите город назначения",
                "failure_text": "{error}\nЕсли хотите вернуться на другой шаг, - напишите /return",
                "handler": "handle_destination_city",
                "next_step": "step_3",
                "prev_step": "step_1"
            },
            "step_3": {
                "text": "Введите желаемую дату вылета в формате dd-mm-yyyy",
                "failure_text": "{error}\nЕсли хотите вернуться на другой шаг, - напишите /return",
                "handler": "handle_input_date",
                "next_step": "step_4",
                "prev_step": "step_2"
            },
            "step_4": {
                "text": "Доступны следующие рейсы:\n{flights}"
                        "\nВведите понравившийся номер рейса:",
                "failure_text": "{error}\nЕсли хотите вернуться на другой шаг, - напишите /return",
                "handler": "handle_flight_number",
                "next_step": "step_5",
                "prev_step": "step_3"
            },
            "step_5": {
                "text": "Введите количество мест (от 1 до 5)",
                "failure_text": "Введено неверное значение.\nВведите значение от 1 до 5"
                                "\nЕсли хотите вернуться на другой шаг, - напишите /return",
                "handler": "handle_places",
                "next_step": "step_6",
                "prev_step": "step_4"
            },
            "step_6": {
                "text": "Напишите комментарий в произвольной форме или отправьте 'Нет', если комментарий не нужен.\n"
                        "Если хотите вернуться на другой шаг, - напишите /return",
                "failure_text": None,
                "handler": "handle_comment",
                "next_step": "step_7",
                "prev_step": "step_5"
            },
            "step_7": {
                "text": "Введите ваше ФИО. На него будет оформлен билет.",
                "failure_text": "ФИО должно состоять из 3-30 букв и дефиса. Попробуйте еще раз.\n",
                "handler": "handle_name",
                "next_step": "step_8",
                "prev_step": 'step_6'
            },
            "step_8": {
                "text": "Уточняем введенные данные. Введите 'да' если данные корректны или 'нет', - если есть ошибки\n"
                        "{input_data}",
                "failure_text": "Введено неверное значение, попробуйте еще раз.\n"
                                "Если хотите вернуться на другой шаг, - напишите /return",
                "handler": "check_data",
                "next_step": "step_9",
                "prev_step": "step_7"
            },
            "step_8*": {
                "text": "Уточните, на какой шаг вы хотите вернуться.\n{input_data}\nВведите номер поля, на которое "
                        "хотите вернуться",
                "failure_text": "{error}",
                "handler": "change_data",
                "next_step": None,
                "prev_step": None
            },
            "step_9": {
                "text": "Введите ваш контактный номер телефона в формате +7-123-456-78-90",
                "failure_text": "{error}",
                "handler": "handle_phone_number",
                "next_step": "step_10",
                "prev_step": "step_8"
            },
            "step_10": {
                "text": "Спасибо за заказ! Вот Ваш билет. Распечатайте его",
                "failure_text": None,
                "handler": None,
                "image": "generate_ticket",
                "next_step": None,
                "prev_step": None
            },
        }
    },
    "forecast": {
        "first_step": "step_1",
        "steps": {
            "step_1": {
                "text": "Введите дату, на которую хотите получить прогноз",
                "failure_text": "{error}\nЕсли хотите вернуться на другой шаг, - напишите /return",
                "handler": "handle_date",
                "next_step": "step_2",
                "prev_step": 'step_1'
            },
            "step_2": {
                "text": "Добавить прогноз в базу данных?",
                "failure_text": "{error}\nЕсли хотите вернуться на другой шаг, - напишите /return",
                "handler": "handle_add_forecast",
                "next_step": "step_3",
                "prev_step": 'step_1'
            },
            "step_3": {
                "text": "Получить прогноз из базы?",
                "failure_text": "{error}\nЕсли хотите вернуться на другой шаг, - напишите /return",
                "handler": "handle_get_forecast",
                "next_step": "step_4",
                "prev_step": 'step_2'
            },
            "step_4": {
                "text": "Создать открытку из прогноза?",
                "failure_text": "{error}\nЕсли хотите вернуться на другой шаг, - напишите /return",
                "handler": "handle_create_postcard",
                "next_step": "step_5",
                "prev_step": 'step_3'
            },
            "step_5": {
                "text": "Вывести прогноз в чат?",
                "failure_text": "{error}\nЕсли хотите вернуться на другой шаг, - напишите /return",
                "handler": "handle_print_forecast",
                "next_step": None,
                "prev_step": 'step_4',
                "print_text": "{text}"
            },
        }
    }
}

DEFAULT_ANSWER = "Не знаю, как на это ответить.\n Напиши '/help' чтобы получить помощь"

DB_CONFIG = dict(
    provider='postgres',
    user='postgres',
    host='localhost',
    database='telegram_bot'
)
