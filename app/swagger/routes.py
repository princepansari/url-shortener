from .src.get_docs import GetDocs

def initialize_swagger_routes(api):
    api.add_resource(GetDocs, "/api/docs")