import logging
import os
from sqlalchemy import text


from app.db.session import SessionDB


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







