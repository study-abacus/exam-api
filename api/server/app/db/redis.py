import redis
import os


class Redis:

    def __init__(self):
        self.client = redis.Redis(host=os.getenv('REDIS_HOST'),\
                                   port=int(os.getenv('REDIS_PORT')),
                                   password=os.getenv('REDIS_PASS'),\
                                   charset="utf-8", decode_responses=True)