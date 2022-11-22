#!/bin/bash

pytest_date=`date +"%Y-%m-%d"`
pytest_time=`date +"%T"`
mkdir -p ./logs/pytest_logs/$pytest_date

python -m pytest -vv | tee ./logs/pytest_logs/$pytest_date/pytest_$pytest_time.log