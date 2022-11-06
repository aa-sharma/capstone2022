# Apollo

A rehabilitation glove with an interactive interface for recovering stroke patients and others with limited hand mobility.

![alt text](./plot.png)

## Edit .env.example file

In order to run the app on your local setup you must rename `.env.example.dev` to `.env.dev`

In order to run the tests on your local setup you must also rename `.env.example.test` to `.env.test` file with your test environment variables.

Next you can change some of the parameters in the environment files as needed, such as usernames and password as these should be set by you, but I would leave
`HOST` and `PORT` parameters alone.

## Install Docker and Docker Compose on your Machine

Docker: https://docs.docker.com/engine/install/
Docker Compose: https://docs.docker.com/compose/install/

## Run Application

There is a file in the root directory called `run-app.sh`. You can start the application, including the server and database simply by typing `./run-app.sh`.
You may or may not need to make it an executable file by running `chmod +x run-app.sh`, though this will only need to be done once.

if everything goes well you should see

`info: MongoDB Connected...` and `info: Server started on port 5000`

Let me know if this works or not, I can help out if needed, i have not tested this on anything except for a mac, but it should work on other machines
all the same.

## Run Tests

There is a file in the root directory called `run-tests.sh`. You can run the tests, which boots up a seperate instance of the database and
server by running `./run-tests.sh`. You may or may not need to make it an executable file by running `chmod +x run-tests.sh`, though this will
only need to be done once.

## Setup Data Processor

You must `cd ./services/python-client` create a python virtual environment, enable it, then install the required dependencies

```
python3 -m venv venv
source ./venv/bin/activate    (macos)
pip3 install -r requirements.txt
```

Set your COM_PORT in `.env` and BAUD_RATE if necessary. Then you can run the program using

```
python3 ./src/main.py
```

## Logs

You can view logs at ./logs

Additionally when running tests, logs will be stored at ./services/tests/logs

## Disclaimer

> uOttawa Electrical Engineering Capstone 2022.

_Eric Hallé-Sherman. Reethi Paul. Ziad Salameh. Aashna Sharma. Lucas Rahn._
