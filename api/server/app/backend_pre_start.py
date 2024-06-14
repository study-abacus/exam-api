import logging
import os
from sqlalchemy import text


from app.db.session import SessionDB
from app.db.redis import Redis


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    try:
        logger.info("Creating initial data")
        _db = SessionDB()
        logger.info("Session established")
        db = _db.get_session()
        select = db.execute(text("SELECT 1"))
        logger.info("Selecting data from database")
        for row in select:
            print(row)
        db.close()
        logger.info("Database connection closed")
        redis = Redis()
        _redis = redis.client
        logger.info("Redis connection established")
        _redis.set("test", "test")
        logger.info("Setting test key in redis")
        _redis.get("test")
        logger.info("Getting test key from redis")
        _redis.delete("test")
        logger.info("Deleting test key from redis")
        _redis.close()
        logger.info("Initial data created")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise e



def main() -> None:
    logger.info("Initializing service")
    init()
    logger.info("Service initialized")


if __name__ == "__main__":
    main()







