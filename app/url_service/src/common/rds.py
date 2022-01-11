import os
import boto3
import psycopg2
from psycopg2.extras import RealDictCursor
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.config import Config


class RDS:

    def __init__(self):
        self.env = Config.ENV
        self.host = Config.RDS_ENDPOINT
        self.user = Config.DBUSER
        self.database = Config.DATABASE
        self.password = Config.PASSWORD
        self.region = Config.REGION
        self.port = int(Config.PORT)

        conn_str = self.get_connection_string()
        self.connection = psycopg2.connect(conn_str)

    def get_connection_string(self):
        env = self.env
        host = self.host
        port = self.port
        user = self.user
        region = self.region
        database = self.database
        password = self.password

        if env != "test":
            client = boto3.client("rds", region_name=region)
            password = client.generate_db_auth_token(DBHostname=host, Port=port, DBUsername=user)

        conn_str = f"host={host} dbname={database} user={user} password={password} port={port}"
        return conn_str

    def get_user_by_email(self, *, email):
        cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        query = "SELECT user_id FROM users WHERE email=%s"
        cursor.execute(query, [email])
        user_id = cursor.fetchone()["user_id"]
        return user_id

    def get_user_by_key(self, *, developer_key):
        cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        query = "SELECT user_id FROM developer_keys WHERE developer_key=%s"
        cursor.execute(query, [developer_key])
        user_id = cursor.fetchone()["user_id"]
        return user_id

    def check_shortened_link(self, *, shortened_link):
        cursor = self.connection.cursor()
        query = "SELECT creation_id FROM creations WHERE shortened_link=%s"
        cursor.execute(query, [shortened_link])
        return cursor.fetchone() is not None

    def add_alias(self, *, user_id, original_link, shortened_link, expiry_duration):
        cursor = self.connection.cursor()
        if expiry_duration:
            query = "INSERT INTO creations (user_id, original_link, shortened_link, expiry_duration)" \
                    " VALUES (%s, %s,%s, %s)"
            cursor.execute(query, [user_id, original_link, shortened_link, expiry_duration])
        else:
            query = "INSERT INTO creations (user_id, original_link, shortened_link) VALUES (%s, %s,%s)"
            cursor.execute(query, [user_id, original_link, shortened_link])
        self.connection.commit()
