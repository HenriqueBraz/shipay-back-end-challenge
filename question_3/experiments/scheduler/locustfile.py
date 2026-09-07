
# doc: https://docs.locust.io/en/stable/api.html

# To run the load test, use the
# following command (adjust TARGET_RPS and USERS as needed):
# TARGET_RPS=50 USERS=10 locust -f question_3/experiments/scheduler/locustfile.py

# ----------------------------------------------------------------------------------

import os
from datetime import datetime, timedelta

from locust import HttpUser, constant_throughput, task

TARGET_RPS = float(os.getenv("TARGET_RPS", "10"))
USERS = int(os.getenv("USERS", "10"))

REQUESTS_PER_USER = TARGET_RPS / USERS


class SchedulerUser(HttpUser):
    host = "http://127.0.0.1:8000"

    # Distribui a taxa desejada entre os usuários virtuais.
    wait_time = constant_throughput(REQUESTS_PER_USER)

    @task
    def schedule_event(self):
        scheduler_datetime = (
            datetime.now() + timedelta(minutes=10)
        ).isoformat()

        self.client.post(
            "/v1/render/scheduler",
            json={
                "scheduler_datetime": scheduler_datetime,
                "event_content": "teste de carga com locust",
            },
        )