#!/bin/bash

sleep 5

pytest_date=`date +"%Y-%m-%d"`
pytest_time=`date +"%T"`
mkdir -p ./logs/pytest_logs/$pytest_date

pytest | tee ./logs/pytest_logs/$pytest_date/pytest_$pytest_time.log