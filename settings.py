import datetime
import os

import pytz


DATABASENAME = "weatherbot.db"
TIMETORUN = datetime.time(hour=8, minute=0, tzinfo=pytz.timezone("Europe/Moscow"))
TOKEN = os.environ.get("TOKEN", "NO TOKEN")
