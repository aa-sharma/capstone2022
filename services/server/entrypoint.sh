#!/bin/bash

if [[ ${NODE_ENV} == "development" ]]; then
  nodemon server.js
elif [[ ${NODE_ENV} == "production" ]]; then
  npm start
fi