from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

import app.helpers.constants as const
from app.helpers.constants import GetField
from app.helpers.email_routines import send_email, build_email

send_mail_router = Router()


@send_mail_router.message(Command(commands=[const.SEND_MAIL]))
async def get_email(message: Message, state: FSMContext):
    if message.from_user.id != const.user_id:
        await message.answer("This bot is not for you!")
        return

    await message.answer("Enter recipient's email:")
    await state.set_state(GetField.waiting_for_email_addr)


@send_mail_router.message(GetField.waiting_for_email_addr)
async def get_subject(message: Message, state: FSMContext):
    await state.update_data(To=message.text)
    await message.answer("Enter message Subject:")
    await state.set_state(GetField.waiting_for_email_subj)


@send_mail_router.message(GetField.waiting_for_email_subj)
async def get_text(message: Message, state: FSMContext):
    await state.update_data(Subject=message.text)
    await message.answer("Enter message text:")
    await state.set_state(GetField.waiting_for_email_text)


@send_mail_router.message(GetField.waiting_for_email_text)
async def send_mail(message: Message, state: FSMContext):
    await state.update_data(Text=message.text)
    data = await state.get_data()

    email_message = build_email(data['To'], data['Subject'], data['Text'])

    if send_email(email_message):
        await message.answer("Email sent!")
    else:
        await message.answer("Wrong email address!")

    await state.update_data({})
    await state.set_state(default_state)
