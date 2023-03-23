from celery import Celery
from os import getenv
import time
from datetime import datetime

REDIS_URL = getenv("REDIS_URL", "redis://localhost:6379")

app = Celery(broker=REDIS_URL, backend=REDIS_URL)


@app.task(name="dummy")
def dummy() -> str:
    time.sleep(10)
    date = datetime.now().strftime("%H:%M:%S")
    return f"hello {date}"
