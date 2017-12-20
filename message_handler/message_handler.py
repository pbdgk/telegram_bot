from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from logs import log_users
from tasks.currency_tasks import Currency


TASKS = {'/currency': Currency}


class BaseMessageHandler:

    def __init__(self, bot, db, message):
        self._bot = bot
        self._db = db
        self.msg = message

    def _restore_user_session(self):
        if self._get_user_session(self.msg['chat_id']):
            self._db.clear_session(self.msg['chat_id'])
        self._db.add_session(self.msg['chat_id'], self.msg['text'])

    def _get_user_session(self, chat_id):
        return self._db.check_session(chat_id)


class ChatHandler(BaseMessageHandler):

    def __init__(self, bot, db, message):
        super().__init__(bot, db, message)

    @property
    def msg(self):
        return self._msg

    @msg.setter
    def msg(self, value):
        self._msg = {'text': value['text'],
                     'date': value['date'],
                     'first_name': value['from']['first_name'],
                     'chat_id': value['from']['id']
                     }

    async def handle(self):
        if self.msg['text'] == '/help' or self.msg['text'] == '/start':
            await self.send_help_message()

        elif self._is_command(self.msg['text']):
            self._restore_user_session()
            session = self._get_user_session(self.msg['chat_id'])
            await self.do_task(*session)
        else:
            session = self._get_user_session(self.msg['chat_id'])
            if session:
                await self.do_task(*session, new_message=self.msg['text'])
            else:
                await self.send_help_message()

    async def do_task(self, chat_id, cls, vars_, new_message=None):
        cls = TASKS.get(cls)
        msg, currency = await cls().do_task(vars_, new_message)
        if msg and not new_message:
            await self._bot.sendMessage(chat_id, msg)
        elif msg and new_message and currency:
            await self.send_inline_query(chat_id, msg, currency)
        else:
            await self._bot.sendMessage(chat_id, 'wrong try again')

    async def send_help_message(self):
        text = 'Hi there!\nPlease choose one of the following commands\n'
        for cmd in TASKS:
            text += cmd + '\n'
        await self._bot.sendMessage(self.msg['chat_id'], text)

    async def send_inline_query(self, chat_id, message, currency):
        buttons = self._generate_markup(currency)
        markup = InlineKeyboardMarkup(inline_keyboard=[buttons])
        await self._bot.sendMessage(chat_id, message, reply_markup=markup)

    @staticmethod
    def _generate_markup(items):
        buttons = list()
        for item in items:
            buttons.append(InlineKeyboardButton(text=item, callback_data=item))
        return buttons

    @staticmethod
    def _is_command(command):
        return command in TASKS


class CallbackHandler(BaseMessageHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def msg(self):
        return self._msg

    @msg.setter
    def msg(self, value):
        self._msg = {'text': value['data'],
                     'date': value['message']['date'],
                     'first_name': value['from']['first_name'],
                     'chat_id': value['from']['id']
                     }

    @log_users
    async def handle(self):
        self._db.update_session(self.msg['chat_id'], self.msg['text'])
        _, TaskCls, user_answers, *_ = self._db.check_session(self.msg['chat_id'])
        TaskCls = TASKS.get(TaskCls)
        inline_query_reply, end = TaskCls().get_reply(user_answers)
        await self._bot.sendMessage(self.msg['chat_id'], inline_query_reply)
        if end:
            self._db.clear_session(self.msg['chat_id'])


def TestFunc():
    X='string'
    y=1
    y+=1
    print ('testing wrong pep8')
