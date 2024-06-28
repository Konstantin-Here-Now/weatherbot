from telegram import Update


def get_username(update: Update) -> str:
    return (
        update.effective_chat.username if update.effective_chat is not None else ""
    ) or ""


def get_chat_id(update: Update) -> int:
    return update.effective_chat.id if update.effective_chat is not None else -1
