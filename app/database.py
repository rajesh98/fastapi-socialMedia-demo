from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#from urllib import quote_plus as urlquote
import urllib.parse
from .config import settings



#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:%s@localhost/fastapi" % urllib.parse.quote_plus('rajesh1234@')

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{urllib.parse.quote_plus(settings.database_password)}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}" 
#print(SQLALCHEMY_DATABASE_URL)
#engine = create_engine('postgres://user:%s@host/database' % urlquote('badpass'))

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
# while True:
# 	try:
# 		conn = psycopg2.connect(host = "localhost", database = 'fastapi', user ='postgres',
# 		password = 'rajesh1234@', cursor_factory=RealDictCursor )

# 		# Open a cursor to perform database operations
# 		cursor = conn.cursor()
# 		print("Success Connection")
# 		break

# 	except:
# 		print("connection filed")
# 		time.sleep(2)
		

