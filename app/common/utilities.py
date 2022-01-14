from datetime import datetime, timezone, timedelta
import re
import uuid
import hashlib
from hashids import Hashids
from app.common.config import Config
import validators

class Utils:

    @staticmethod
    def validate_email(email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.fullmatch(regex, email)

    @staticmethod
    def validate_password(password):
        if (len(password) >= 8):
            lower = upper = special = digit = 0
            for char in password:

                if (char.islower()):
                    lower += 1

                if (char.isupper()):
                    upper += 1

                if (char.isdigit()):
                    digit += 1

                if (char in '!@#$%^&*()~'):
                    special += 1

            if (lower >= 1 and upper >= 1 and special >= 1 and digit >= 1
                    and lower + special + upper + digit == len(password)):
                return True
        return False

    @staticmethod
    def get_uuid():
        return str(uuid.uuid4())

    @staticmethod
    def encode(*, url):
        custom_alphabet = "23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"
        hashids = Hashids(salt=Config.SECRET_ENCODE, alphabet=custom_alphabet)

        digest = hashlib.md5((url + Utils.get_uuid()).encode()).hexdigest()
        encoded_string = hashids.encode(int(digest, 16))

        return encoded_string[:Config.URL_LENGTH]

    @staticmethod
    def remove_prefix(string, prefix):
        if string.startswith(prefix):
            return string[len(prefix):]
        return None

    @staticmethod
    def is_valid_url(*, url):
        if validators.url(url):
            return True
        if not url.startswith("http") and validators.url("https://" + url):
            return True
        return False

    @staticmethod
    def is_expired(*, creation_time, expiry_duration):
        current_time = datetime.now(timezone.utc)
        if current_time > creation_time + timedelta(days=expiry_duration):
            return True
        return False
