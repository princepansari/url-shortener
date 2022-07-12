import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Config:

    DOMAIN_NAME = os.environ.get("DOMAIN_NAME") or "https://shortify.tech/"
    COMPANY_NAME = os.environ.get("COMPANY_NAME") or "shortify"
    READ_URL = DOMAIN_NAME + "url/"
    NETLOC1 = os.environ.get("NETLOC1") or "shortify.tech"
    NETLOC2 = os.environ.get("NETLOC2") or "www.shortify.tech"
    # Common config
    TMP_DIR = os.environ.get("TMP_DIR") or "/tmp"
    ENV = os.environ.get("ENV") or "test"

    # RDS config
    REGION = os.environ.get("REGION")
    RDS_ENDPOINT = os.environ.get("RDS_ENDPOINT")
    PORT = os.environ.get("PORT")
    DBUSER = os.environ.get("DBUSER")
    DATABASE = os.environ.get("DATABASE")
    PASSWORD = os.environ.get("PASSWORD")

    #email config
    FROM_EMAIL = "shortify.tech@gmail.com"
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
    REFRESH_TOKEN = os.environ.get("REFRESH_TOKEN")
    DEVELOPER_KEY_GEN_SECRET = os.environ.get('DEVELOPER_KEY_GEN_SECRET')

    #JWT config
    EXPIRE_AFTER_DAYS = os.environ.get('EXPIRE_AFTER_DAYS') or 7

    #URL Service
    CHARACTERS_FOR_ALIAS = os.environ.get("CHARACTERS_FOR_ALIAS") or "23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"
    URL_LENGTH = os.environ.get("URL_LENGTH") or 6
    MAX_URL_LENGTH = os.environ.get("MAX_URL_LENGTH") or 10
    SECRET_ENCODE = os.environ.get("SECRET_ENCODE") or "aEjFb182bHUWsuibJBXBVZDHU"
    MIN_EXPIRY_DURATION = os.environ.get("MIN_EXPIRY_DURATION") or 1
    MAX_EXPIRY_DURATION = os.environ.get("MAX_EXPIRY_DURATION") or 30

    #OTP config
    OTP_DIGIT_SPACE = os.environ.get('OTP_DIGIT_SPACE') or '0123456789'
