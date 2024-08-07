import json

import redis

from config import SETTINGS

redis_client = redis.Redis(
    host=SETTINGS.REDIS_HOST,
    port=SETTINGS.REDIS_PORT,
    db=SETTINGS.REDIS_DATABASE,
)

if __name__ == '__main__':

    print(redis_client.info())
    redis_client.setex(f"user:{123}",
                       100,
                       value=json.dumps({34: 'dima', 45: "mimo"}))

    redis_client.set(name=f"user:{1230}",
                     value=json.dumps({34: 'dima', 45: "mimo"}))


