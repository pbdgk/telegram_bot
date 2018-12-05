import logging
import time
logger = logging.getLogger(__name__)

logging.basicConfig(filename='info.log', filemode='w', level=logging.INFO)


def log_users(fn):
    async def wrapper(obj, *args, **kwargs):
        msg = getattr(obj, 'msg', None)
        date = time.ctime(msg['date'])
        chat_id = msg['chat_id']
        user_name = msg['first_name']
        logging.info('{} || {} || {}'.format(date, chat_id, user_name))
        return await fn(obj, *args, **kwargs)
    return wrapper
