from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

DB_URL = "mysql+pymysql://root:root@192.168.49.2:30007/rain"

class DBconn:
    def __init__(self):
        self.engine = create_engine(DB_URL, pool_recycle = 500)

    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn