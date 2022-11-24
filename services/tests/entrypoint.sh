#!/bin/bash

# pytest_date=`date +"%Y-%m-%d"`
# pytest_time=`date +"%T"`
# mkdir -p ./logs/pytest_logs/$pytest_date
# touch ./logs/pytest_logs/$pytest_date/pytest_$pytest_time.log

# python -m pytest -p pytest_session2file --session2file=./logs/pytest_logs/$pytest_date/pytest_$pytest_time.log
python -m pytest
