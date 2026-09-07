# ---------------------------------------------------------------------

# To run the FastAPI application, use the following command:
# uvicorn question_3.experiments.scheduler.app:app --reload

# To start the RQ worker, use the following command in a separate terminal:
# rq worker default --with-scheduler


# You can test the scheduler endpoint using the following curl command 
# (adjust scheduler_datetime and event_content as needed):

# curl -X POST http://127.0.0.1:8000/v1/render/scheduler -H "Content-Type: application/json" -d '{"scheduler_datetime":"2026-09-06T19:50:00","event_content":"teste do scheduler executado!"}'


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel
from redis import Redis
from rq import Queue

app = FastAPI()

redis_connection = Redis(host="localhost", port=6379)
queue = Queue(name="default", connection=redis_connection)


class SchedulerRequest(BaseModel):
    scheduler_datetime: datetime
    event_content: str


@app.post("/v1/render/scheduler")
def scheduler(request: SchedulerRequest):
    # trocado publish_event por print para fins de teste, 
    # pois não temos a função publish_event implementada
    job = queue.enqueue_at(
        request.scheduler_datetime,
        print,
        request.event_content,
    )

    return {
        "job_id": job.id,
        "status": "scheduled",
    }