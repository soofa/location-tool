from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import importlib

if os.environ.get('APP_ENVIRONMENT') is not None:
    config_module = importlib.import_module(
        'config.{}'.format(os.environ.get('APP_ENVIRONMENT'))
    )
else:
    config_module = importlib.import_module('config.development')


engine = create_engine(config_module.DATABASE,
                       client_encoding='utf8')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def truncate_database(session):
    """Remove all data from the database"""
    tables = Base.metadata.tables.keys()
    sql = "TRUNCATE TABLE {}".format(','.join(tables))
    session.execute(sql)
