from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from celery.result import AsyncResult
from redis import Redis
from redis.lock import Lock as RedisLock

from . import task

app = FastAPI()

redis_instance = Redis.from_url(task.REDIS_URL)
lock = RedisLock(name="__task__", redis=redis_instance)

CURRENT_TASK_KEY = "current_task"


class TaskOut(BaseModel):
    task_id: str
    status: str


@app.get("/start")
def start() -> TaskOut:
    try:
        if not lock.acquire(blocking_timeout=10):
            raise HTTPException(500, detail="could not acquire lock")
        last_id = redis_instance.get(CURRENT_TASK_KEY)
        if last_id is None or task.app.AsyncResult(last_id).ready():
            r = task.dummy.delay()
            redis_instance.set(CURRENT_TASK_KEY, r.task_id)
            return _to_task_out(r)
        else:
            raise HTTPException(400, detail="already a task running sorry.")
    finally:
        lock.release()


@app.get("/status")
def status(task_id: str | None = None) -> TaskOut:
    r = task.app.AsyncResult(task_id or redis_instance.get(CURRENT_TASK_KEY))
    return _to_task_out(r)


@app.get("/cancel")
def cancel(task_id: str | None = None) -> str:
    task_id = task_id or redis_instance.get(CURRENT_TASK_KEY)
    task.app.control.revoke(task_id.decode("utf-8"), terminate=True, signal="SIGKILL")
    return "ok"


def _to_task_out(r: AsyncResult):
    return TaskOut(task_id=r.task_id, status=r.status)
