# Apollo

A rehabilitation glove with an interactive interface for recovering stroke patients and others with limited hand mobility.

![alt text](./plot.png)

## Locally Run

If on windows/linux go to https://www.mongodb.com/docs/mongodb-shell/install/ for details on how to install mongodb on your system. Otherwise
Docker might be set up in the future to support easily running the entire application with one command on any machine, we will have to see how much this is in demand.

### Install MongoDB

`brew tap mongodb/brew` - macos

`brew install mongodb-community@6.0` - macos

### Install dependencies

`cd services/server`

`npm i`

### Start MongoDB

`brew services start mongodb-community@6.0` - macos

### Start NodeJS

`npm start`

if all steps were successful, this should start a nodejs server thats connected to a local mongodb deployment. You should see
"MongoDB Connected...", "Server started on port 5000"

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
