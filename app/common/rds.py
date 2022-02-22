from datetime import datetime, timezone, timedelta
import boto3
import psycopg2
from psycopg2.extras import RealDictCursor
from app.common.config import Config
from app.common.utilities import Utils
import hashlib

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
        query = "INSERT INTO users (email, password) VALUES (%s, %s) "\
                "ON CONFLICT (email) " \
                "DO UPDATE SET password = %s "\
                "RETURNING user_id"
        cursor.execute(query, [email, password, password])
        self.connection.commit()
        user_id = cursor.fetchone()['user_id']
        return user_id


    def update_last_login(self, *, email):
        cursor = self.connection.cursor()
        query = "UPDATE users SET last_login=%s WHERE email=%s"
        curr_time = datetime.utcnow()
        cursor.execute(query, [curr_time, email])
        self.connection.commit()

    def upsert_dev_key(self, user_id, developer_key):
        cursor = self.connection.cursor()
        query = "INSERT INTO developer_keys (user_id, developer_key) VALUES (%s, %s) " \
                "ON CONFLICT (user_id) " \
                "DO UPDATE SET developer_key = %s"
        cursor.execute(query, [user_id, developer_key, developer_key])
        self.connection.commit()

    def save_otp(self, *, user_id, otp):
        cursor = self.connection.cursor()
        query = "INSERT INTO signup_verification (user_id, otp) VALUES (%s, %s) " \
                "ON CONFLICT (user_id) " \
                "DO UPDATE SET otp = %s"
        cursor.execute(query, [user_id, otp, otp])
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

    def get_user_by_email(self, *, email):
        cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        query = "SELECT user_id FROM users WHERE email=%s"
        cursor.execute(query, [email])
        user = cursor.fetchone()
        return user['user_id'] if user else None

    def get_user_by_key(self, *, developer_key):
        developer_key_hash = hashlib.sha256(developer_key.encode()).hexdigest()
        cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        query = "SELECT user_id FROM developer_keys WHERE developer_key=%s"
        cursor.execute(query, [developer_key_hash])
        user = cursor.fetchone()
        return user['user_id'] if user else None

    def is_shortened_link_exists(self, *, shortened_link):
        cursor = self.connection.cursor()
        query = "SELECT creation_id FROM creations WHERE shortened_link=%s"
        cursor.execute(query, [shortened_link])
        return cursor.fetchone() is not None

    def add_shortened_link(self, *, user_id, original_link, shortened_link, expiry_duration):
        cursor = self.connection.cursor()
        if expiry_duration:
            query = "INSERT INTO creations (user_id, original_link, shortened_link, expiry_duration) " \
                    "VALUES (%s, %s,%s, %s) ON CONFLICT (shortened_link) DO NOTHING"
            cursor.execute(query, [user_id, original_link, shortened_link, expiry_duration])
        else:
            query = "INSERT INTO creations (user_id, original_link, shortened_link) VALUES (%s, %s,%s) " \
                    "ON CONFLICT (shortened_link) DO NOTHING"
            cursor.execute(query, [user_id, original_link, shortened_link])
        self.connection.commit()
        return True if cursor.rowcount else False

    def get_user_links(self, *, user_id):
        def get_cursor():
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            query = "SELECT original_link, shortened_link, created_at, expiry_duration, visits " \
                    "FROM creations WHERE user_id=%s"
            cursor.execute(query, [user_id])
            return cursor
        cursor = get_cursor()
        user_links = {'user_links': []}
        while True:
            row = cursor.fetchone()
            if not row:
                break
            if not Utils.is_expired(creation_time=row['created_at'], expiry_duration=row['expiry_duration']):
                user_links['user_links'].append({
                    'original_link': row['original_link'],
                    'shortened_link': Config.READ_URL + row['shortened_link'],
                    'created_at': row['created_at'].isoformat(),
                    'expiry_duration': row['expiry_duration'],
                    'visits': row['visits']
                })
        return user_links

    def delete_shortened_link(self, *, user_id, shortened_link):
        cursor = self.connection.cursor()
        query = "DELETE FROM creations WHERE user_id=%s and shortened_link=%s"
        cursor.execute(query, [user_id, shortened_link])
        self.connection.commit()
        return cursor.rowcount

    def get_original_link(self, *, shortened_link):
        cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        query = "UPDATE creations SET visits=visits+1 WHERE shortened_link=%s RETURNING *"
        try:
            cursor.execute(query, [shortened_link])
        except psycopg2.Error as e:
            self.connection.commit()
            return None
        self.connection.commit()
        data = cursor.fetchone()
        if data and not Utils.is_expired(creation_time=data['created_at'], expiry_duration=data['expiry_duration']):
            return data['original_link']
        return None

    def get_link_detail(self, *, link):
        cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        query = "SELECT * FROM malicious_links WHERE link=%s"
        cursor.execute(query, [link])
        link_detail = cursor.fetchone()
        return link_detail

    def update_quota(self, *, user_id):
        cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        query = "SELECT * FROM user_quota WHERE user_id=%s"
        cursor.execute(query, [user_id])
        data = cursor.fetchone()
        if not data:
            query = "INSERT INTO user_quota (user_id) VALUES (%s)"
            cursor.execute(query, [user_id])
            self.connection.commit()
        elif data['last_updated'] + timedelta(hours=24) < datetime.now(timezone.utc):
            query = "UPDATE user_quota SET quota=%s, last_updated=%s WHERE user_id=%s"
            cursor.execute(query, [0, datetime.now(timezone.utc), user_id])
            self.connection.commit()
        query = "UPDATE user_quota SET quota=quota+1 WHERE user_id=%s"
        try:
            cursor.execute(query, [user_id])
        except psycopg2.Error as e:
            self.connection.commit()
            return False
        self.connection.commit()
        return True

    def subtract_user_quota(self, *, user_id):
        cursor = self.connection.cursor()
        query = "UPDATE user_quota SET quota=quota-1 WHERE user_id=%s"
        cursor.execute(query, [user_id])
        self.connection.commit()
