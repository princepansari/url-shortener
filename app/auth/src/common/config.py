import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Config:

    # Common config
    TMP_DIR = os.environ.get("TMP_DIR") or "/tmp"
    ENV = os.environ.get("ENV") or "test"

    # RDS config
    REGION = os.environ.get("REGION") or "us-east-2"
    RDS_ENDPOINT = os.environ.get("RDS_ENDPOINT") or "https://mydatabase.cvqngijdukip.us-east-2.rds.amazonaws.com/"
    PORT = os.environ.get("PORT") or "5432"
    DBUSER = os.environ.get("DBUSER") or "unicorn"
    DATABASE = os.environ.get("DATABASE") or "unicorn_db"
    PASSWORD = os.environ.get("PASSWORD") or "welcome123"