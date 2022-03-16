# xbot
[![Pylint](https://github.com/mlkra/xbot/actions/workflows/pylint.yml/badge.svg)](https://github.com/mlkra/xbot/actions/workflows/pylint.yml)
[![test](https://github.com/mlkra/xbot/actions/workflows/test.yml/badge.svg)](https://github.com/mlkra/xbot/actions/workflows/test.yml)

Bot for tracking products' availability at x-kom.pl.

## Requirements
Python 3.10+

## Configuration
xbot can be configured using environment variables:
- `SMTP_HOST`, `SMTP_PORT` - host and port of smtp server used to send email notifications

## Runing
Use provided `docker-compose.yml`.
