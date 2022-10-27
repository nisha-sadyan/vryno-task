from email import message
from fastapi import FastAPI

# from enum import Enum
from pydantic import BaseModel

from prod_cons import producer_consumer
import asyncio


class FooApp(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pika_client = producer_consumer(
            process_callable=self.log_incoming_message,
            send_topic="accounts-in",
            receive_topic="accounts-out",
        )

    @classmethod
    async def log_incoming_message(cls, message: dict):
        print(message)
        """Method to do something meaningful with the incoming message"""
        # logger.info('Here we got incoming message %s', message)


app = FooApp()
students = {}


class student(BaseModel):
    Fname: str
    Lname: str
    phone: int


@app.post("/create-student")
async def create_student(
    student_id: int,
    payload: student,
):
    if student_id in students:
        return {"error": "student exist"}

    await app.pika_client.send({"message": payload.dict()})
    # await app.pika_client.process_incoming_message(payload)
    return {"status": "ok"}

    # students[student_id]= payload
    # return students[student_id]


@app.on_event("startup")
async def startup():
    await asyncio.sleep(5)
    loop = asyncio.get_running_loop()
    print("hello all")
    task = loop.create_task(app.pika_client.receive(loop))

    await task
