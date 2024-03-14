docker run \
    -it \
    --rm \
    --name redis \
    --net redis \
    -p 6379:6379 \
    -v ${PWD}/config:/etc/redis/ \
    -v redis:/data/ \
    redis:7.2.4-alpine \
    redis-server /etc/redis/redis.conf
