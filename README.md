# SWGOps

SWGOps is a set of Discord bots that make life easier in a galaxy far, far away.

## Requirements

* [docker] (https://docs.docker.com/get-docker/)
* [docker-compose](https://docs.docker.com/compose/install/)

## Configuration

* Create a new Discord bot, follow [this guide](https://discordpy.readthedocs.io/en/stable/discord.html#inviting-your-bot)
* Copy the bot token into your '.env' file

## Build

```
docker-compose build
```

### Make data volumes

```
./mk_volumes
```

### Remove data volumes

```
./rm_volumes.sh
```

## Run

```
docker-compose up -d
```

## Stop

```
docker-compose down
```