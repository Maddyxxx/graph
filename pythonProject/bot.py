
from pony.orm import db_session

import handlers
import settings
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

from models import UserState, Ticket


class Bot(object):

    def __init__(self, token):
        self.updater = Updater(token=token)  # заводим апдейтера
        handler = MessageHandler(Filters.text | Filters.command, self.run)
        self.updater.dispatcher.add_handler(handler)  # ставим обработчик всех текстовых сообщений
        self.default_steps = ['step_5', 'step_6', 'step_7']  # при изменении данных, эти шаги по дефолту не меняются,
        # пользователь их заного не проходит

    def start(self):
        self.updater.start_polling()

    @db_session
    def run(self, update, context):
        chat_id = update.message.chat_id
        text = update.message.text
        state = UserState.get(chat_id=str(chat_id))
        for intent in settings.INTENTS:
            if any(token in text.lower() for token in intent['tokens']):
                if text == intent['tokens']:
                    self.start_scenario(chat_id, context.bot, intent['scenario'], text)
                    break
                else:
                    if intent['answer']:
                        context.bot.sendMessage(chat_id=chat_id, text=intent['answer'])
                        break
        else:
            if state is not None:
                self.continue_scenario(text, context.bot, state, chat_id)
            else:
                context.bot.sendMessage(chat_id=chat_id, text=settings.DEFAULT_ANSWER)

    def send_step(self, step, chat_id, bot, text, context):
        if 'text' in step:
            bot.sendMessage(chat_id=chat_id, text=step['text'].format(**context))
        if 'image' in step:
            handler = getattr(handlers, step['image'])
            image = handler(text, context)
            bot.send_photo(chat_id, photo=open(image, 'rb'))

    def start_scenario(self, chat_id, bot, scenario_name, text):
        scenario = settings.SCENARIOS[scenario_name]
        first_step = scenario['first_step']
        step = scenario['steps'][first_step]
        UserState(chat_id=str(chat_id), scenario_name=scenario_name, step_name=first_step, context={})
        self.send_step(step, chat_id, bot, text, context={})

    def continue_scenario(self, text, bot, state, chat_id):
        print(text, state.step_name)
        steps = settings.SCENARIOS[state.scenario_name]["steps"]
        step = steps[state.step_name]
        handler = getattr(handlers, step['handler'])
        response = handler(text, state.context)
        if response == 'next':  # если шаг пройден
            next_step = steps[step['next_step']]
            self.send_step(next_step, chat_id, bot, text, state.context)
            if next_step['next_step']:
                # switch to next step
                state.step_name = step['next_step']
            else:
                # finish scenario
                if state.scenario_name == 'make a ticket':
                    done_steps = state.context["done_steps"]
                    Ticket(
                        dep_city=done_steps['dep_city'],
                        dest_city=done_steps['dest_city'],
                        fly_date=done_steps['fly_date'],
                        flight=done_steps['flight'],
                        places=done_steps['places'],
                        comment=done_steps['comment'],
                        name=done_steps['name'],
                        phone_number=done_steps['phone_number']
                    )
                elif state.scenario_name == 'forecast':
                    bot.sendMessage(chat_id=chat_id, text=state.context['forecast'])
                state.delete()

        elif response == 'back':  # шаг назад
            next_step = steps[step['prev_step']]
            state.step_name = step['prev_step']
            self.send_step(next_step, chat_id, bot, text, state.context)

        elif response == 'change':  # изменение данных
            next_step = state.context['next_step']
            step = steps[next_step]
            state.step_name = next_step
            self.send_step(step, chat_id, bot, text, state.context)
            if next_step in self.default_steps:
                step['next_step'] = 'step_8'

        elif response == 'return':  # запускаем доп шаг если данные не верны
            step = 'step_8*'
            next_step = steps[step]
            state.step_name = step
            self.send_step(next_step, chat_id, bot, text, state.context)
        else:
            text_to_send = step['failure_text'].format(**state.context)
            bot.sendMessage(chat_id, text_to_send)


if __name__ == "__main__":
    bot = Bot(settings.TOKEN)
    bot.start()
