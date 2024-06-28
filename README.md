# WeatherBot

## Quick start
1. Paste your bot token from [BotFather](https://telegram.me/BotFather) to `.env.example` and rename it:
```sh
mv .env.example .env
```

2. Create file `weatherbot.db`:
```sh
touch weatherbot.db
```

3. Start docker container:
```sh
docker compose up -d --build
```