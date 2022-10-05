# Apollo

A rehabilitation glove with an interactive interface for recovering stroke patients and others with limited hand mobility.

![alt text](./plot.png)

## Locally Run

### Edit .env.example file

In order to run the app on your local setup you must rename `.env.example` to `.env.dev`

Next you can change some of the parameters in the environment file as needed, such as usernames and password as these should be set by you.

### Install Docker and Docker Compose

Docker: https://docs.docker.com/engine/install/
Docker Compose: https://docs.docker.com/compose/install/

### Run Docker Compose

Use Docker compose to bootup the server and database

`docker compose -f docker-compose.dev.yml up --build`

if everything goes well you should see

`info: MongoDB Connected...` and `info: Server started on port 5000`

Let me know if this works or not, I can help out if needed

## Run Tests

Tests were created using pytest. Currently the suite requires that mongodb is set up and running, and the NodeJS/Express server is running
and ready to receive API calls

### Setup local virutal environment

`python3 -m venv venv` - macos/maybe windows?

### Activate virtual environment

`source ./venv/bin/active` - macos/maybe windows?

### Install Dependencies

`pip3 install -r requirements.txt`

### Run Tests

`pytest`

> uOttawa Electrical Engineering Capstone 2022.

_Eric Hallé-Sherman. Reethi Paul. Ziad Salameh. Aashna Sharma. Lucas Rahn._
