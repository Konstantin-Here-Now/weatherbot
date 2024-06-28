from dataclasses import dataclass
import logging
import aiosqlite

from settings import DATABASENAME


@dataclass
class Subscriber:
    chat_id: int
    username: str


class SubscriberDB:
    """Class for accessing db table with the same name"""

    @staticmethod
    async def try_subscribe(username: str, chat_id: int) -> bool:
        try:
            async with aiosqlite.connect(DATABASENAME) as conn:
                cursor = await conn.cursor()
                await cursor.execute(
                    """
                    INSERT INTO subscriber (id, username)
                    VALUES(?, ?)
                    """,
                    [chat_id, username],
                )
                await conn.commit()
                return True
        except aiosqlite.Error as e:
            logging.error(e)
            return False

    @staticmethod
    async def try_unsubscribe(chat_id: int) -> bool:
        try:
            async with aiosqlite.connect(DATABASENAME) as conn:
                cursor = await conn.cursor()
                await cursor.execute(
                    """
                    DELETE FROM subscriber
                    WHERE id = ?
                    """,
                    [chat_id],
                )
                await conn.commit()
                return True
        except aiosqlite.Error as e:
            logging.error(e)
            return False

    @staticmethod
    async def get_all_subscribers() -> list[Subscriber]:
        subscribers: list[Subscriber] = []
        try:
            async with aiosqlite.connect(DATABASENAME) as conn:
                cursor = await conn.cursor()
                await cursor.execute(
                    """
                    SELECT id, username FROM subscriber
                    """
                )
                subscribers = [Subscriber(sub[0], sub[1]) for sub in await cursor.fetchall()]
        except aiosqlite.Error as e:
            logging.error(e)
        return subscribers
