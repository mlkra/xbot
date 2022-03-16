#!/bin/bash
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

COMPOSE_FILE="docker-compose.dev.yml"

export XKOM_URL=http://localhost:5000
export XKOM_API_URL=http://localhost:5000
export SMTP_HOST=localhost
export SMTP_PORT=1025

case $1 in
"build")
    docker-compose -f $COMPOSE_FILE build
    ;;
"down")
    docker-compose -f $COMPOSE_FILE down
    ;;
"e2e-test")
    cd xbot
    python -m pytest ./tests/e2e
    ;;
"integration-test")
    cd xbot
    python -m pytest ./tests/integration
    ;;
"test")
    cd xbot
    python -m pytest ./tests
    ;;
"unit-test")
    cd xbot
    python -m pytest ./tests/unit
    ;;
"up")
    docker-compose -f $COMPOSE_FILE up
    ;;
"upd")
    docker-compose -f $COMPOSE_FILE up -d
    ;;
*)
    echo "Invalid command"
    exit 1
    ;;
esac
