# DESIRE6G Service Orchestrator

## Overview

The `DESIRE6G` Service Orchestrator serves as a middleware for handling Service deployment and coordinating messages between the various SMO components. It utilizes FastAPI for handling HTTP requests and provides functionalities for processing file uploads and managing messaging flows.

### Components

- **app.py**: The main script for the SO. It defines the FastAPI endpoints for Service Graph registration and forwarding.
- **messaging/rabbitmq.py**: Module for interacting with RabbitMQ messaging system. It provides methods for sending and receiving messages asynchronously.
- **requirements.txt**: Specifies the required Python packages for the application.


### Requirements
- Python 3.7 or higher
- FastAPI
- Requests

#### Installation

Clone the repository:

```bash
git clone https://github.com/nubispc/desire6g-so
```

#### Install dependencies:

```bash
pip install fastapi requests uvicorn
```

#### Usage

Run the FastAPI application using uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### API

The DESIRE6G SO provides endpoints for deploying services, listing deployed services, and retrieving information about deployed services.

#### Endpoints

`POST /default_service/`: Uploads a file and processes it.

`POST /default_service_id/`: Deploys a new service by its ID.

`DELETE /default_service_id/{service_id}`: Deletes service based on the ID returned from the `deployed_services` endpoint.

`GET /deployed_services`: Lists all deployed services.

`GET /deployed_services/{service_id}`: Retrieves information about a deployed service by ID.


#### Environment Variables

- `TOPOLOGY_ENDPOINT`: URL of the topology service (default: localhost).
- `IML_ENDPOINT`: URL of the IML service (default: localhost:5000/iml/yaml/deploy).
- `SERVICE_NAME`: (Optional) Specifies the name of the service. Default is `default_service`.
- `SERVICE_NAME_ID`: (Optional) Specifies the name of the service. Default is `default_service`.
- `RABBITMQ_HOST`: Specifies the host address of the RabbitMQ messaging system.

#### Deployment

Deploy the FastAPI application using Kubernetes:

`kubectl create -f desire6g-so.yml`

### Example Usage

#### Create Site:

```bash
curl -X 'POST' \
  'http://localhost:32007/nodes/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "site_id": "desire6g-site",
  "cpu": 8,
  "mem": 32,
  "storage": 1024
}'
```

#### Upload Service Graph:

```bash
curl -X POST -F "file=@demo_nsd.sg.yaml" http://localhost:32006/upload
```

#### Deploy Service:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"json_data": {"type": "service_graph", "name": "demo_nsd.sg.yaml", "site_id": "desire6g-site"}}' http://localhost:32008/main_id/ | jq
```

#### Query Deployments:

```bash
curl http://localhost:32008/deployed_services
```

Output:

```json
{"deployed_services":[2]}
```

#### Get Info on Deployed Service:

```bash
curl http://localhost:32008/deployed_services/2
```

Output:

```json
{
  "service_name": "2",
  "details": {
    "status": "deployed",
    "service_name": "Digital Twin Demo",
    "file_name": "demo_nsd.sg.yaml",
    "site_id": "desire6g-site"
  }
}
```

#### Delete deployed service

```bash
curl http://localhost:320008/main_d/2
```

Output:
```json
{
  "message": "Service deleted",
  "service_id": 2
}
```

### Container build

Build the Docker image:
    ```
    docker build -t desire6g-so -f Dockerfile .
    ```

### Folder Structure
- `app.py`: Main script for the SO.
- `requirements.txt`: Specifies the required Python packages.
- `Dockerfile`: Dockerfile for building the Docker image.
- `messaging/`: Contains modules for handling messaging with RabbitMQ and Kafka.
    - `__init__.py`: Initialization file for the messaging package.
    - `rabbitmq.py`: Module for interacting with RabbitMQ messaging system.
    - `kafka.py`: Module for interacting with Kafka messaging system.

### Contributing

Contributions to the `DESIRE6G` SO are welcome! Please feel free to open an issue or submit a pull request for any improvements or features you'd like to add.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
