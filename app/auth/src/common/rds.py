from datetime import datetime
import os
import boto3
import psycopg2
from psycopg2.extras import RealDictCursor
import sys
from app.auth.src.common.config import Config


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

    def get_user(self, *, email):
        def get_cursor():
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            query = ("SELECT * FROM users WHERE email=%s")
            cursor.execute(query, [email])
            return cursor

        cursor = get_cursor()
        user = cursor.fetchone()
        return user

    def create_user(self, *, email, password):
        cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        query = "INSERT INTO users (email, password) VALUES (%s, %s) RETURNING user_id"
        cursor.execute(query, [email, password])
        self.connection.commit()
        user_id = cursor.fetchone()['user_id']
        return user_id

    def is_user_exists(self, *, email):
        def get_cursor():
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            query = ("SELECT * FROM users WHERE email=%s")
            cursor.execute(query, [email])
            return cursor

        cursor = get_cursor()
        user = cursor.fetchone()
        return user is not None


    def update_last_login(self, *, email):
        cursor = self.connection.cursor()
        query = "UPDATE users SET last_login=%s WHERE email=%s"
        curr_time = datetime.utcnow()
        cursor.execute(query, [curr_time, email])
        self.connection.commit()

    def upsert_dev_key(self, user_id, developer_key):
        cursor = self.connection.cursor()
        query = "INSERT INTO developer_keys (user_id, developer_key) VALUES (%s, %s) " \
                "ON CONFLICT (user_id)" \
                "DO UPDATE SET developer_key = %s"
        cursor.execute(query, [user_id, developer_key, developer_key])
        self.connection.commit()

    def save_otp(self, *, user_id, otp):
        cursor = self.connection.cursor()
        query = "INSERT INTO signup_verification (user_id, otp) VALUES (%s, %s)"
        cursor.execute(query, [user_id, otp])
        self.connection.commit()

    def get_user_otp(self, user_id):
        def get_cursor():
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            query = ("SELECT otp FROM signup_verification WHERE user_id=%s")
            cursor.execute(query, [user_id])
            return cursor

        cursor = get_cursor()
        row = cursor.fetchone()
        otp = row['otp']
        return otp

    def update_verification_status(self, *, email):
        cursor = self.connection.cursor()
        query = "UPDATE users SET verified=true WHERE email=%s"
        cursor.execute(query, [email])
        self.connection.commit()