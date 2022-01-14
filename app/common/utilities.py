import re
import uuid
import hashlib
from hashids import Hashids
from app.common.config import Config


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
        else:
            return None
