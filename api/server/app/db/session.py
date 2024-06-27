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
                                                    
                                          pool_recycle=300,      
                                          pool_pre_ping=True   
                                )
           


      def get_session(self):
            session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            return session_local()




     



