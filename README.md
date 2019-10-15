# jaspurrbot
[![Build Status](https://travis-ci.org/SebRut/jaspurrbot.svg?branch=master)](https://travis-ci.org/SebRut/jaspurrbot)
`jaspurrbot` is a just-for-fun telegram bot filled with insides jokes for a telegram group with my friends.

# Setup
## Docker
The bot is run via docker and you need your own [telegram bot token](https://core.telegram.org/bots/api).
### docker-compose.yml
```
version: "3"

services:
  telegram-bot:
    container_name: telegram-bot
    hostname: telegram-bot
    build:
      - context: .
      - dockerfile: ./Dockerfile
    image: sebrut/jaspurrbot
    environment:
      - JASPURR_TG_TOKEN=
    restart: unless-stopped
```
