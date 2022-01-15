from flask_restful import Resource
from flask import Response, render_template

class GetDocs(Resource):

    def get(self):
        return Response(response=render_template('swaggerui.html'))
