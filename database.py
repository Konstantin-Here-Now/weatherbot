import logging
import aiosqlite

from settings import DATABASENAME


async def prepare_db():
    await create_database(DATABASENAME)
    await create_tables(DATABASENAME)


async def create_database(db_name: str):
    """Create a database connection to an SQLite database"""
    conn = None
    try:
        conn = await aiosqlite.connect(db_name)
        logging.info(aiosqlite.sqlite_version)
    except aiosqlite.Error as e:
        logging.error(e)
        raise e
    finally:
        if conn:
            await conn.close()


async def create_tables(db_name: str):
    """Create database table"""
    sql_statements = [
        """CREATE TABLE IF NOT EXISTS subscriber (
                id INTEGER PRIMARY KEY, 
                username TEXT NOT NULL
        )""",
    ]
    try:
        async with aiosqlite.connect(db_name) as conn:
            cursor = await conn.cursor()
            for statement in sql_statements:
                await cursor.execute(statement)
            await conn.commit()
            logging.info("Database tables created")
    except aiosqlite.Error as e:
        logging.error(e)
        raise e
