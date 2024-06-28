import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from database import prepare_db
from settings import TOKEN
from subscriber import SubscriberDB
from utils import get_chat_id, get_username

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = get_chat_id(update)
    response_message = (
        "Привет! Я бот, умеющий показывать погоду на день. "
        + "Если хочешь подписаться на погоду, используй /subscribe."
    )
    await context.bot.send_message(
        chat_id=chat_id,
        text=response_message,
    )


async def subcribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = get_chat_id(update)
    username = get_username(update)

    is_successful = await SubscriberDB.try_subscribe(username, chat_id)
    if is_successful:
        logging.info(f"{username} {chat_id} subscribed.")
        response_message = "Вы успешно подписались на прогноз погоды! Чтобы отписаться, воспользуйтесь /unsubscribe"
    else:
        response_message = "Произошла проблема подписки, попробуйте снова"

    await context.bot.send_message(
        chat_id=chat_id,
        text=response_message,
    )


async def unsubcribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = get_username(update)
    chat_id = get_chat_id(update)
    is_successful = await SubscriberDB.try_unsubscribe(chat_id)
    if is_successful:
        logging.info(f"{username} unsubscribed.")
        await context.bot.send_message(
            chat_id=chat_id, text="Вы успешно отписались от рассылки!"
        )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Произошла ошибка в процессе отписки, попробуйте снова.",
        )


async def send_message(context: ContextTypes.DEFAULT_TYPE):
    subscribers = await SubscriberDB.get_all_subscribers()
    for subscriber in subscribers:
        logging.info(f"Weather sent to {subscriber.username}.")
        await context.bot.send_message(chat_id=subscriber.chat_id, text="Ежеминутное сообщение")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(prepare_db())
    application = ApplicationBuilder().token(TOKEN).build()
    job_queue = application.job_queue

    handlers = [
        CommandHandler("start", start),
        CommandHandler("subscribe", subcribe),
        CommandHandler("unsubscribe", unsubcribe),
    ]
    for handler in handlers:
        application.add_handler(handler)

    job_minute = job_queue.run_repeating(send_message, interval=60, first=10)  # type: ignore
    application.run_polling()
