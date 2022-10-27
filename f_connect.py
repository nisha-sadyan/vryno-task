import asyncio
import pika
import aio_pika
import json
from prod_cons import producer_consumer
from d_handeler import data
import uvicorn

async def abc(message: dict):
    print(message)
    print(type(message))
    save_obj = db.insert(**message["message"])
    print("i am save_obj",dict(save_obj))
    print("data inserted to database")
    
    
    await pika_client.send({"message": save_obj})
        # await asyncio.Future()

    

if __name__ == "__main__":
    pika_client = producer_consumer(
        process_callable=abc, send_topic="accounts-out", receive_topic="accounts-in"
    )
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(pika_client.receive(loop))
        db = data()
        db.create()
        loop.run_forever()
    except asyncio.CancelledError as err:
            print(err)
            raise
    
    
