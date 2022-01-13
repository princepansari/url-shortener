import uuid
import hashlib
from hashids import Hashids
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.config import Config


class Utils:

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
