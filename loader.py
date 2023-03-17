import config
import logging
import erp
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bd.sql import db_start

class AuthMiddleware(BaseMiddleware):

    def __init__(self):
        BaseMiddleware.__init__(self)

    async def on_process_message(self, message: types.Message, data: dict):
        if not await erp.get_id_erp(message.from_user.id):
            raise CancelHandler()

bot = Bot(config.BOT_TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    )
