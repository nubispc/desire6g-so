from fastapi import FastAPI, UploadFile, File, BackgroundTasks, Body, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional, Dict, List
from pydantic import BaseModel
import os, re
import requests
import base64
from messaging import get_messaging_system

from io import BytesIO

app = FastAPI()

messaging = get_messaging_system()

class Item(BaseModel):
    json_data: dict

# In-memory state storage
request_states = {}
deployed_services = {}

TOPOLOGY_SERVICE_URL = "http://" + os.getenv('TOPOLOGY_ENDPOINT', 'localhost') + ":8000"
IML_ENDPOINT = os.getenv('IML_ENDPOINT', 'http://localhost:5000')

@app.post(f"/{os.getenv('SERVICE_NAME', 'default_service')}/")
async def process_upload_and_get_result(item: UploadFile = File(...)):
    input_yaml = await item.read()
    request_id = len(request_states) + 1  # Simple incrementing ID
    request_states[request_id] = {"status": "processing", "input": input_yaml, "output": None}

    await messaging.send_message(input_yaml)

    response_content = await messaging.receive_message()
    if response_content:
        print(f"Received final message: {response_content}")
        request_states[request_id]["status"] = "completed"
        request_states[request_id]["output"] = response_content
        return JSONResponse(content={"message": "Received", "data": response_content})
    else:
        print("No final message received.")
        request_states[request_id]["status"] = "failed"
        return JSONResponse(content={"message": "No Message"})

@app.post(f"/{os.getenv('SERVICE_NAME_ID', 'default_service_id')}/")
async def service_by_id(item: Item = Body(...)):
    input_json = item.json_data
    request_id = len(request_states) + 1
    request_states[request_id] = {"status": "processing", "input": input_json, "output": None}

    file_type = input_json["type"]
    file_name = input_json["name"]
    file_content = download_file_from_service(file_type, file_name)

    await messaging.send_message(base64.b64encode(file_content.encode()))

    site_id = input_json["site_id"]
    # Check if the site exists in the topology component
    response = requests.get(f"{TOPOLOGY_SERVICE_URL}/nodes/{site_id}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Site not found")
    
 
    response_content = await messaging.receive_message()
    if response_content:
        #print(f"Received final message: {response_content}")
        request_states[request_id]["status"] = "completed"
        request_states[request_id]["output"] = response_content

        # Convert the string content to a file-like object
        file_like_object = BytesIO(base64.b64decode(response_content).decode().encode('utf-8'))
        files = {'file': ('demo_nsd.yml', file_like_object)}

        iml_response = requests.post(f"{IML_ENDPOINT}", files=files)
        #print(iml_response.json())
        #import pdb;pdb.set_trace()

        json_data = iml_response.json()['response']
        # Use a regular expression to find key-value pairs
        pattern = r'(\w+):\s*([^,}]+)'
        matches = re.findall(pattern, json_data)

        # Convert the matches to a dictionary
        structured_dict = {key: value for key, value in matches}

        service_id = int(structured_dict["id"])
        service_name = structured_dict["Deployed"]
        deployed_services[service_id] = {"status": "deployed", "service_name": service_name, "file_name": file_name, "site_id": site_id }

        #return JSONResponse(content={"message": "Received", "data": iml_response.json(), "file": base64.b64decode(response_content).decode(), "site_id": site_id, "service_id": service_id })
        return JSONResponse(content={"message": "Received", "status": "deployed", "service_name": service_name, "file_name": file_name, "site_id": site_id})
    else:
        print("No final message received.")
        request_states[request_id]["status"] = "failed"
        return JSONResponse(content={"message": "No Message"})

@app.delete(f"/{os.getenv('SERVICE_NAME_ID', 'default_service_id')}/{{service_id}}")
async def delete_service(service_id: int):
    if service_id not in deployed_services:
        raise HTTPException(status_code=404, detail="Service not found")

    # Simulate service deletion process, like making a call to an external service
    # For example: response = requests.delete(f"{IML_ENDPOINT}/{service_id}")
    # Assuming the service gets successfully deleted

    response = requests.delete(f"{IML_ENDPOINT}/{service_id}")

    # Remove the service from the deployed_services dictionary
    del deployed_services[service_id]

    return JSONResponse(content={"message": "Service deleted", "service_id": service_id})

@app.get("/deployed_services")
async def list_deployed_services():
    return JSONResponse(content={"deployed_services": list(deployed_services.keys())})

@app.get("/deployed_services/{service_id}")
async def get_deployed_service(service_id: str):
    service_info = deployed_services[int(service_id)]
    if service_info:
        return JSONResponse(content={"service_name": service_id, "details": service_info})
    else:
        raise HTTPException(status_code=404, detail="Service not found")

@app.post("/deploy_service/")
async def deploy_service(service_name: str = Body(...), site_id: str = Body(...)):
    # Check if the site exists in the topology component
    response = requests.get(f"{TOPOLOGY_SERVICE_URL}/nodes/{site_id}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Site not found")
    
    deployed_services[service_name] = {"status": "deployed", "site_id": site_id}
    return JSONResponse(content={"message": "Service deployed", "service": service_name, "site_id": site_id})

@app.post("/retract_service/")
async def retract_service(service_name: str = Body(...)):
    if service_name in deployed_services:
        del deployed_services[service_name]
        return JSONResponse(content={"message": "Service retracted", "service": service_name})
    else:
        return JSONResponse(content={"message": "Service not found", "service": service_name})

def download_file_from_service(file_type, file_name):
    scip = os.getenv('SERVICE_CATALOG')
    url = f'http://{scip}:8000/file/{file_type}/{file_name}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["file_content"]
    else:
        print(f"Failed to download file: {response.text}")
        return None

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
