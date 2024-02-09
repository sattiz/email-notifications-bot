from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import app.helpers.constants as const

main_menu_router = Router()


@main_menu_router.message(Command(const.START))
async def start(message: Message):
    if message.from_user.id != const.user_id:
        await message.answer("This bot is not for you!")
        return

    await message.answer(f"Hello user {const.user_id}!")


@main_menu_router.message(StateFilter(None), Command(commands=[const.CANCEL]))
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    if message.from_user.id != const.user_id:
        await message.answer("This bot is not for you!")
        return

    await state.set_data({})
    await message.answer(text="Nothing to cancel")


@main_menu_router.message(Command(commands=[const.CANCEL]))
async def cmd_cancel(message: Message, state: FSMContext):
    if message.from_user.id != const.user_id:
        await message.answer("This bot is not for you!")
        return

    await state.clear()
    await message.answer(text="Operation cancelled")


@main_menu_router.message(Command(commands=[const.DATA]))
async def show_personal_data(message: Message):
    if message.from_user.id != const.user_id:
        await message.answer("This bot is not for you!")
        return

    text = f"Email: {const.mailAddress}\n" + f"Imap Mail Server: {const.imapMailServer}\n" + \
           f"Imap Mail Port: {const.imapMailPort} \n" + f"Smtp Mail Server: {const.smtpMailServer}\n" + \
           f"Smtp Mail Port: {const.smtpMailPort} \n" + f"Password: {const.mailPassword} \n" + \
           f"ChatID: {message.chat.id}\n" + f"UserID: {const.user_id}"

    await message.answer(text)
