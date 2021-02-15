#!/usr/bin/env bash
export MONGODB_NAME=${MONGODB_NAME:-"hitarget"}
poetry run uvicorn hitarget.main:app --port ${API_PORT:="5000"} --host ${API_HOST:="0.0.0.0"} $@
