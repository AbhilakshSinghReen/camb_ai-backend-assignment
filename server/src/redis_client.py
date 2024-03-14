from os import environ

from redis import Redis


redis_host = 'localhost'
redis_port = 6379
redis_db = 0 

redis_client = Redis(host=redis_host, port=redis_port, db=redis_db, password=None, decode_responses=True)
