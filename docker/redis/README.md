# Redis

## Docker Hub Links

- [Redis (Official Image)](https://hub.docker.com/_/redis)
- [Redis Insight](https://hub.docker.com/r/redislabs/redisinsight)

## Documentation Links

- [Redis](https://phoenixnap.com/kb/docker-redis)
- [RedisInsight](https://developer.redis.com/explore/redisinsight/getting-started/)

## Run

To run server and web admin tool, use Docker Compose.

```zsh
docker-compose up -d
```

To view the logs of either container, list all running containers, and use the hash code to view the logs for the container.

```zsh
docker ps -a

docker logs -f <CONTAINER_ID>
```





