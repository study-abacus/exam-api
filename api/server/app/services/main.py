from sqlalchemy.orm import Session

class DBSessionContext(object):
    def __init__(self, db: Session, cache=None):
        self.db = db
        self.cache = cache


class AppService(DBSessionContext):
    pass


class AppCRUD(DBSessionContext):
    pass