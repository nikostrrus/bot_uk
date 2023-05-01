from loader import bot, db_start, AuthMiddleware


async def on_shutdown(dp):
    await bot.close()

async def on_startup(_):
    await db_start()

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    dp.middleware.setup(AuthMiddleware())
    executor.start_polling(dp,
                           on_startup=on_startup,
                           on_shutdown=on_shutdown,
                           skip_updates=True)
    
