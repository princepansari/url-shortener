import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.generate_url import GenerateURL, CreateURL


def url_service_routes(api):
    api.add_resource(GenerateURL, '/generate_url')
    api.add_resource(CreateURL, '/create_url')

