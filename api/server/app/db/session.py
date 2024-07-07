from abc import abstractmethod
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import urllib
from sqlalchemy.engine import URL




class Database:


      def __init__(self) -> None:
            self.host_server = os.environ.get('DB_HOST')
            self.db_server_port = urllib.parse.quote_plus(str(os.environ.get('db_server_port', '5432')))
            self.database_name = os.environ.get('DB_NAME')
            self.db_username = urllib.parse.quote_plus(os.environ.get('DB_USER'))
            self.db_password = urllib.parse.quote_plus(os.environ.get('DB_PASS'))
            self.ssl_mode = urllib.parse.quote_plus(str(os.environ.get('ssl_mode','prefer')))
            self.SQLALCHEMY_DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(self.db_username, self.db_password, self.host_server, self.db_server_port, self.database_name, self.ssl_mode)


      @abstractmethod
      def get_session(self):
            pass


class SessionDB(Database):


      def __init__(self) -> None:
            super().__init__()


            self.engine = create_engine(self.SQLALCHEMY_DATABASE_URL,
                                         pool_size=30,           # Set pool_size to 30, respecting the max_connections limit of PostgreSQL
                                          max_overflow=10,        # Adjust max_overflow accordingly based on peak load scenarios
                                          pool_timeout=30,        # Timeout in seconds before giving up on getting a connection from the pool
                                          pool_recycle=1800,      # Recycle connections after 30 minutes (1800 seconds)
                                          pool_pre_ping=True ,   # Check the connection health before use (recommended for PostgreSQL)
                                          echo=False               # Set to True to see SQL statements echoed to stdout (for debugging)
                                )
           


      def get_session(self):
            session_local = sessionmaker(bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False)
            return session_local()




     



