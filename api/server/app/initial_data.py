import logging


from app.db.init_db import init_db
from app.db.session import SessionDB


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)




def init() -> None:
    _db = SessionDB()
    init_db(_db)


def main() -> None:
    logger.info("Creating initial tables")
    init()
    logger.info("Initial data created")
   


if __name__ == "__main__":
    main()





