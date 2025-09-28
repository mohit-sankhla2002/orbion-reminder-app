from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
load_dotenv()

db_url = os.environ.get("MYSQL_URL")

if not db_url:
    raise ValueError("MYSQL_URL environment variable not set")

engine = create_engine(db_url, echo=True)

def get_engine():
    return engine
