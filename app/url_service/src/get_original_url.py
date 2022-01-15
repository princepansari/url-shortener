from flask import request, redirect
from flask_restful import Resource
from http import HTTPStatus
from app.common.rds import RDS


class GetOriginalUrl(Resource):
    def __init__(self):
        self.rds = RDS()

    def get(self, shortened_link):
        original_link = self.rds.get_original_link(shortened_link=shortened_link)
        if original_link is None:
            # TODO - change the json output to the html page for invalid link
            return {'error': 'Invalid shortened link'}, HTTPStatus.BAD_REQUEST

        is_malicious, malicious_class = GetOriginalUrlUtils.is_malicious_link(self.rds, original_link)

        if is_malicious:
            # TODO - change the json output to the html page for malicious link
            return {'original_link': original_link,
                    'is_malicious': is_malicious,
                    'class_of_malicious_link': malicious_class}, HTTPStatus.OK

        return redirect(original_link, code=302)


class GetOriginalUrlDev(Resource):
    def __init__(self):
        self.rds = RDS()

    def get(self, shortened_link):
        original_link = self.rds.get_original_link(shortened_link=shortened_link)
        if original_link is None:
            return {'error': 'Invalid shortened link'}, HTTPStatus.BAD_REQUEST

        is_malicious, malicious_class = GetOriginalUrlUtils.is_malicious_link(self.rds, original_link)

        return {'original_link': original_link,
                'is_malicious': is_malicious,
                'class_of_malicious_link': malicious_class}, HTTPStatus.OK


class GetOriginalUrlUtils:

    @staticmethod
    def is_malicious_link(*, rds, link):
        link_detail = rds.get_link_detail(link=link)
        return (True, link_detail['class_of_malicious_link']) if link_detail else (False, None)

