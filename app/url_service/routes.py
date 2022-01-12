import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.generate_url import GenerateUrl, GenerateUrlDev
from src.get_original_url import GetOriginalUrl
from src.get_my_urls import GetMyUrls, GetMyUrlsDev
from src.delete_url import DeleteUrl, DeleteUrlDev


def url_service_routes(api):
    api.add_resource(GenerateUrl, '/generate_url')
    api.add_resource(GenerateUrlDev, '/generate_url_dev')

    api.add_resource(GetOriginalUrl, '/get_original_url')

    api.add_resource(GetMyUrls, '/get_my_urls')
    api.add_resource(GetMyUrlsDev, '/get_my_urls_dev')

    api.add_resource(DeleteUrl, '/delete_url')
    api.add_resource(DeleteUrlDev, '/delete_url_dev')
