import asyncio

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import app.helpers.constants as consts
from app.handlers.main_menu_handlers import main_menu_router
from app.handlers.send_mail import send_mail_router
from app.helpers.constants import token
from app.helpers.email_routines import check_emails_job


async def main():
    bot = Bot(token)
    dp = Dispatcher()
    scheduler = AsyncIOScheduler()

    dp.include_router(main_menu_router)
    dp.include_router(send_mail_router)

    scheduler.add_job(check_emails_job, "interval", seconds=consts.timeout, args=(bot,))
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    print('Bot started.')
