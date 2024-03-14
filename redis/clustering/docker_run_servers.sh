# redis-0
docker run \
    -d \
    --rm \
    --name redis-0 \
    --net redis \
    -v ${PWD}/redis-0/config:/etc/redis/ \
    redis:7.2.4-alpine \
    redis-server /etc/redis/redis.conf

# redis-1
docker run \
    -d \
    --rm \
    --name redis-1 \
    --net redis \
    -v ${PWD}/redis-1/config:/etc/redis/ \
    redis:7.2.4-alpine \
    redis-server /etc/redis/redis.conf

# redis-2
docker run \
    -d \
    --rm \
    --name redis-2 \
    --net redis \
    -v ${PWD}/redis-2/config:/etc/redis/ \
    redis:7.2.4-alpine \
    redis-server /etc/redis/redis.conf
