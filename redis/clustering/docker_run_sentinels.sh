# sentinel-0
docker run \
    -d \
    --rm \
    --name sentinel-0 \
    --net redis \
    -v ${PWD}/sentinel-0/config:/etc/redis/ \
    redis:7.2.4-alpine \
    redis-sentinel /etc/redis/sentinel.conf

# sentinel-1
docker run \
    -d \
    --rm \
    --name sentinel-1 \
    --net redis \
    -v ${PWD}/sentinel-1/config:/etc/redis/ \
    redis:7.2.4-alpine \
    redis-sentinel /etc/redis/sentinel.conf

# sentinel-2
docker run \
    -d \
    --rm \
    --name sentinel-2 \
    --net redis \
    -v ${PWD}/sentinel-2/config:/etc/redis/ \
    redis:7.2.4-alpine \
    redis-sentinel /etc/redis/sentinel.conf
