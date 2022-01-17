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
    REGION = os.environ.get("REGION") or "us-east-2"
    RDS_ENDPOINT = os.environ.get("RDS_ENDPOINT") or "mydatabase.cvqngijdukip.us-east-2.rds.amazonaws.com"
    PORT = os.environ.get("PORT") or "5432"
    DBUSER = os.environ.get("DBUSER") or "unicorn"
    DATABASE = os.environ.get("DATABASE") or "unicorn_db"
    PASSWORD = os.environ.get("PASSWORD") or "welcome123"

    #email config
    FROM_EMAIL = "shortify.tech@gmail.com"
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID") or "393388259530-e13a3lv6fje5mc87itt3d9fkj83j3gaa.apps.googleusercontent.com"
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET") or "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"
    REFRESH_TOKEN = os.environ.get("REFRESH_TOKEN") or "1//04eHJ8tySHcAoCgYIARAAGAQSNwF-L9IrBT3fOprU0yW0Arsy5brsrwFuQP5JH4MtIarWApQX-D_WPRl6N7zMlzD-2OAH-yDP9Bo"
    #dev key gen config
    DEVELOPER_KEY_GEN_SECRET = os.environ.get('DEVELOPER_KEY_GEN_SECRET') or "AAXCDESA"

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