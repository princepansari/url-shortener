import os
import boto3
import psycopg2
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


    def get_users(self, *, include_processed=False):
        def get_cursor():
            cursor = self.connection.cursor()
            query = ("")
            cursor.execute(query, [])
            return cursor

        def get_row(cursor, row):
            return {str(name[0]): value for name, value in zip(cursor.description, row)}

        cursor = get_cursor()
        while True:
            row = cursor.fetchone()
            if not row:
                break
            user = get_row(cursor, row)
            yield user

