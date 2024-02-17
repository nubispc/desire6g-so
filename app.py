from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import UploadFile, File
from typing import List, Dict
import os
from messaging import get_messaging_system
from models import TodoItem

app = FastAPI()

messaging = get_messaging_system()

@app.post(f"/{os.getenv('SERVICE_NAME', 'default_service')}/")
async def process_upload_and_get_result(item: UploadFile = File(...)):
    input_yaml = await item.read()
    await messaging.send_message(input_yaml)

    response_content = await messaging.receive_message()
    if response_content:
        print(f"Received final message: {response_content}")
        return JSONResponse(content={"message": "Received", "data": response_content})
    else:
        print("No final message received.")
        return JSONResponse(content={"message": "No Message"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
