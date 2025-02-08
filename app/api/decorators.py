from functools import wraps
from flask_restx import Resource, Api, fields
from flask import request, current_app
from .models import (
    release_input, release_output, error_response, success_response,
    search_input, search_response, torrent_info
)

def document_endpoint(namespace, description=None, auth_required=True, responses=None):
    """
    Decorator to document Flask routes in Swagger UI
    
    Args:
        namespace: The API namespace to add this endpoint to
        description: Endpoint description
        auth_required: Whether authentication is required
        responses: Dictionary of possible responses
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        # Get endpoint URL and methods
        url = getattr(f, 'rule', '').replace('/api/', '')
        methods = getattr(f, 'methods', ['GET'])
        endpoint = getattr(f, '__name__', '')

        # Create Resource class for this endpoint
        @namespace.route(url, endpoint=endpoint)
        class DocumentedEndpoint(Resource):
            # Define expected models based on endpoint
            endpoint_models = {
                'get_titles': {'response': release_output},
                'add_release': {'request': release_input, 'response': success_response},
                'edit_release': {'request': release_input, 'response': success_response},
                'delete_release': {'request': release_input, 'response': success_response},
                'update_release': {'request': release_input, 'response': success_response},
                'search_releases': {
                    'request': search_input,
                    'response': search_response
                },
                'torrent_info_all_releases': {
                    'response': {
                        'data': fields.List(fields.Nested(torrent_info))
                    }
                }
            }

            # Add method handlers
            for method in methods:
                method = method.lower()
                if method == 'get':
                    @namespace.doc(
                        description=description or f.__doc__,
                        responses={
                            200: ('Success', endpoint_models.get(endpoint, {}).get('response', success_response)),
                            400: ('Bad Request', error_response),
                            401: ('Unauthorized', error_response),
                            500: ('Server Error', error_response)
                        },
                        security=['bearerAuth', 'apiKey'] if auth_required else None
                    )
                    def get(self, *args, **kwargs):
                        return f(*args, **kwargs)

                elif method == 'post':
                    @namespace.doc(
                        description=description or f.__doc__,
                        responses={
                            200: ('Success', endpoint_models.get(endpoint, {}).get('response', success_response)),
                            400: ('Bad Request', error_response),
                            401: ('Unauthorized', error_response),
                            500: ('Server Error', error_response)
                        },
                        security=['bearerAuth', 'apiKey'] if auth_required else None
                    )
                    @namespace.expect(endpoint_models.get(endpoint, {}).get('request', None))
                    def post(self, *args, **kwargs):
                        return f(*args, **kwargs)

                elif method == 'put':
                    @namespace.doc(
                        description=description or f.__doc__,
                        responses={
                            200: ('Success', endpoint_models.get(endpoint, {}).get('response', success_response)),
                            400: ('Bad Request', error_response),
                            401: ('Unauthorized', error_response),
                            500: ('Server Error', error_response)
                        },
                        security=['bearerAuth', 'apiKey'] if auth_required else None
                    )
                    @namespace.expect(endpoint_models.get(endpoint, {}).get('request', None))
                    def put(self, *args, **kwargs):
                        return f(*args, **kwargs)

                elif method == 'delete':
                    @namespace.doc(
                        description=description or f.__doc__,
                        responses={
                            200: ('Success', endpoint_models.get(endpoint, {}).get('response', success_response)),
                            400: ('Bad Request', error_response),
                            401: ('Unauthorized', error_response),
                            500: ('Server Error', error_response)
                        },
                        security=['bearerAuth', 'apiKey'] if auth_required else None
                    )
                    @namespace.expect(endpoint_models.get(endpoint, {}).get('request', None))
                    def delete(self, *args, **kwargs):
                        return f(*args, **kwargs)

        return wrapper
    return decorator 