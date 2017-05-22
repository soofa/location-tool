from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import importlib

app_environment = os.environ.get('APP_ENVIRONMENT')
if app_environment is None:
    app_environment = 'development'
env_config = importlib.import_module('config.{}'.format(app_environment))


engine = create_engine(env_config.DATABASE,
                       client_encoding='utf8')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
