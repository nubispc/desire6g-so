# msrv-main: File Upload and Messaging Middleware

## Overview

The `msrv-main` application serves as a middleware for handling file uploads and coordinating messaging between different systems. It utilizes FastAPI for handling HTTP requests and provides functionalities for processing file uploads and managing messaging flows.

### Functionality

- **File Upload Handling**: Accepts file uploads via HTTP POST requests and processes them.
- **Messaging Coordination**: Acts as a mediator for sending and receiving messages between systems such as RabbitMQ.
- **Asynchronous Processing**: Utilizes asynchronous programming for efficient handling of file uploads and messaging operations.

### Components

- **app.py**: The main script for the `msrv-main` service. It defines the FastAPI endpoints for file upload processing and messaging coordination.
- **messaging/rabbitmq.py**: Module for interacting with RabbitMQ messaging system. It provides methods for sending and receiving messages asynchronously.
- **requirements.txt**: Specifies the required Python packages for the application.

### Usage

1. **File Upload**: Send a file upload request to the `/service_name/` endpoint using HTTP POST method. The service name can be customized via environment variable (`SERVICE_NAME`).
2. **Message Processing**: The uploaded file is processed and forwarded to the messaging system for further handling.
3. **Result Retrieval**: Once processing is complete, the final result message is received from the messaging system and returned as a JSON response.

### Environment Variables

- **SERVICE_NAME**: (Optional) Specifies the name of the service. Default is `default_service`.
- **RABBITMQ_HOST**: Specifies the host address of the RabbitMQ messaging system.

### Deployment

The application can be deployed using Docker. The provided `Dockerfile.msrv-main` sets up a container environment for running the `msrv-main` service. Build the Docker image using `docker build -t msrv-main -f Dockerfile.msrv-main .` and run the container using `docker run -p8000:8000 -it --rm --link rabbitmq-service:rabbitmq-service -e SERVICE_NAME=main msrv-main`.

### Dependencies

Ensure that the necessary Python dependencies specified in `requirements.txt` are installed. You can install them using `pip install -r requirements.txt`.

## Usage
1. Build the Docker image:
    ```
    docker build -t msrv-main -f Dockerfile.msrv-main .
    ```
2. Run the Docker container:
    ```
    docker run -p8000:8000 -it --rm --link rabbitmq-service:rabbitmq-service -e SERVICE_NAME=main msrv-main
    ```
3. Monitor the logs for messaging activity and errors.

## Folder Structure
- `app.py`: Main script for the msrv-main service.
- `requirements.txt`: Specifies the required Python packages.
- `Dockerfile.msrv-main`: Dockerfile for building the Docker image.
- `messaging/`: Contains modules for handling messaging with RabbitMQ and Kafka.
    - `__init__.py`: Initialization file for the messaging package.
    - `rabbitmq.py`: Module for interacting with RabbitMQ messaging system.
    - `kafka.py`: Module for interacting with Kafka messaging system.

### Contributing

Contributions to the `msrv-main` application are welcome! Please feel free to open an issue or submit a pull request for any improvements or features you'd like to add.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.