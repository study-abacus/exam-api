import logging
from db import base

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enable SQLAlchemy logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


def init_db(db) -> None:
    base.Base.metadata.create_all(bind=db.engine)
    if db:
        print("Session established")


    else:
        logger.warning(
            "Cannot create tables for database connection"
        )



