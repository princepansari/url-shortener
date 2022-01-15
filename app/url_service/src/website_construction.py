from flask_restful import Resource
from flask import render_template, Response


class WebsiteConstruction(Resource):
    def __init__(self):
        pass

    def get(self):
        return Response(response=render_template('construction.html'))
