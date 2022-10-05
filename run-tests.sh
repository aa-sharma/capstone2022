#!/bin/bash

docker-compose --env-file .env.test -f docker-compose.test.yml up --build \
    --abort-on-container-exit \
    --exit-code-from test-suite
    