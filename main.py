import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

TOKEN = os.environ.get("TOKEN")
SUBCRIBERS = []

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет! Я бот, умеющий показывать погоду на день в определенное время. Если хочешь подписаться на погоду, используй /subscribe.",
    )


async def subcribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Опа-опа-опа")
    SUBCRIBERS.append(update.effective_chat.id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Вы успешно подписались на прогноз погоды! Чтобы отписаться, воспользуйтесь /unsubscribe",
    )


async def unsubcribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Опа-опа-опа")
    chat_id = update.effective_chat.id
    if chat_id in SUBCRIBERS:
        SUBCRIBERS.remove(chat_id)
        await context.bot.send_message(
            chat_id=chat_id, text="Вы успешно отписались от рассылки!"
        )
    else:
        await context.bot.send_message(
            chat_id=chat_id, text="Вы не можете отписаться, потому что вы не подписаны."
        )


async def send_message(context: ContextTypes.DEFAULT_TYPE):
    for subscriber in SUBCRIBERS:
        await context.bot.send_message(chat_id=subscriber, text="Ежеминутное сообщение")


if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()
    job_queue = application.job_queue

    handlers = [
        CommandHandler("start", start),
        CommandHandler("subscribe", subcribe),
        CommandHandler("unsubscribe", unsubcribe),
    ]
    for handler in handlers:
        application.add_handler(handler)

    job_minute = job_queue.run_repeating(send_message, interval=60, first=10)
    application.run_polling()
