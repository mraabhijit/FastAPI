from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_SQLITE3_DATABASE_URL = "sqlite:///./todos.db"
# Pattern = "db://username:password@hostadress/ApplicationDatabaseName"
SQLALCHEMY_POSTGRES_DATABASE_URL = "postgresql://postgres:postgres@localhost/TodoAppDatabase"


db = 'postgres'

if db == 'Sqlite3':
    engine = create_engine(
        SQLALCHEMY_SQLITE3_DATABASE_URL,
        connect_args={'check_same_thread': False} # to allow multiple threads to use the same conn
    )
elif db == 'postgres':
    engine = create_engine(
        SQLALCHEMY_POSTGRES_DATABASE_URL
    )

SessionLocal = sessionmaker(
    autocommit=False, # autocommit controls transaction behavior
    autoflush=False, # autoflush determines when changes are written to the database
    bind=engine
)

# create a base class with common attributes 
# and behaviors required for SQLAlchemy’s ORM functionality
Base = declarative_base()