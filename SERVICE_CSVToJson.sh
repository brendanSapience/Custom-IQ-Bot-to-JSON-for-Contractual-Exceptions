#!/bin/sh
export FLASK_APP="./services/SERVICE_CSVToJson.py"
export FLASK_ENV="development"
flask run --port=5007
