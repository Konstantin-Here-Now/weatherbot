import asyncio
import os
import telegram

async def main():
    bot = telegram.Bot(os.environ["TOKEN"])
    async with bot:
        print(await bot.get_me())


if __name__ == '__main__':
    asyncio.run(main())
