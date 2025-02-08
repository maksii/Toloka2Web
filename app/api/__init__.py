from flask_restx import Api, fields, Resource
from flask import Blueprint, current_app
from flask_jwt_extended import create_access_token, create_refresh_token

# Create a blueprint for the API
api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(
    api_bp,
    version='1.0',
    title='Toloka2MediaServer API',
    description='''
    API for managing Toloka2MediaServer.
    
    ## Authentication
    The API supports two authentication methods:
    1. **JWT Token** (Recommended): Obtain a token via `/api/auth/login` and use it in the Authorization header
    2. **API Key**: Use your API key in the Authorization header
    
    ### Using JWT Authentication:
    1. Call `/api/auth/login` with your username and password
    2. Copy the access_token from the response
    3. Click the "Authorize" button at the top
    4. In the "bearerAuth" section, enter: `Bearer your_token_here`
    5. Click "Authorize" to save
    
    All subsequent requests will include your JWT token.
    ''',
    doc='/docs',
    authorizations={
        'bearerAuth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
        },
        'apiKey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'X-API-KEY',
            'description': "Your API key"
        }
    },
    security=['bearerAuth', 'apiKey']
)

# Authentication models
login_model = api.model('Login', {
    'username': fields.String(required=True, description='User username'),
    'password': fields.String(required=True, description='User password'),
    'remember_me': fields.Boolean(required=False, description='Remember me flag')
})

token_response = api.model('TokenResponse', {
    'access_token': fields.String(description='JWT access token'),
    'refresh_token': fields.String(description='JWT refresh token'),
    'user': fields.Nested(api.model('UserInfo', {
        'id': fields.Integer(description='User ID'),
        'username': fields.String(description='Username'),
        'roles': fields.String(description='User roles')
    }))
})

error_response = api.model('ErrorResponse', {
    'error': fields.String(description='Error message'),
    'code': fields.String(description='Error code')
})

# Create namespaces for existing route groups
auth_ns = api.namespace('auth', 
    description='Authentication operations',
    decorators=[]  # No auth required for this namespace
)
releases_ns = api.namespace('releases', description='Release operations')
settings_ns = api.namespace('settings', description='Settings operations')
anime_ns = api.namespace('anime', description='Anime operations')
stream_ns = api.namespace('stream', description='Streaming operations')
studio_ns = api.namespace('studio', description='Studio operations')
toloka_ns = api.namespace('toloka', description='Toloka operations')
mal_ns = api.namespace('mal', description='MyAnimeList operations')
tmdb_ns = api.namespace('tmdb', description='TMDB operations')
users_ns = api.namespace('users', description='User operations')

# Import routes to register them with the API
from . import routes

# Add login endpoint to auth namespace
@auth_ns.route('/login')
class Login(Resource):
    @api.doc('login', 
        responses={
            200: ('Success', token_response),
            401: ('Authentication failed', error_response)
        }
    )
    @api.expect(login_model)
    def post(self):
        """
        Login to get JWT tokens
        
        This endpoint allows you to obtain JWT tokens by providing your username and password.
        The tokens can then be used to authenticate other API calls.
        """
        from flask import request
        from app.models.user import User
        
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        remember = data.get('remember_me', False)
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            access_token = create_access_token(
                identity=str(user.id),
                additional_claims={
                    'username': user.username,
                    'roles': user.roles
                }
            )
            refresh_token = create_refresh_token(
                identity=str(user.id),
                additional_claims={
                    'username': user.username,
                    'roles': user.roles
                }
            )
            
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'roles': user.roles
                }
            }
            
        return {'error': 'Invalid username or password', 'code': 'invalid_credentials'}, 401 

# Add refresh token endpoint to auth namespace
@auth_ns.route('/refresh')
class TokenRefresh(Resource):
    @api.doc('refresh_token',
        responses={
            200: ('Success', token_response),
            401: ('Authentication failed', error_response)
        }
    )
    def post(self):
        """
        Refresh access token
        
        Use this endpoint with your refresh token to get a new access token.
        The refresh token should be provided in the Authorization header as 'Bearer <refresh_token>'.
        """
        from flask_jwt_extended import get_jwt_identity, get_jwt, verify_jwt_in_request
        from app.models.user import User
        
        try:
            verify_jwt_in_request(refresh=True)
            
            # Get user info
            current_user_id = get_jwt_identity()
            jwt = get_jwt()
            
            # Check if token is in blocklist
            from .routes.auth import token_blocklist
            jti = jwt.get('jti')
            if jti in token_blocklist:
                return {'error': 'Token has been revoked', 'code': 'token_revoked'}, 401
            
            user = User.query.get(int(current_user_id))
            if not user:
                return {'error': 'User not found', 'code': 'user_not_found'}, 404
            
            # Create new access token
            access_token = create_access_token(
                identity=str(user.id),
                additional_claims={
                    'username': user.username,
                    'roles': user.roles
                }
            )
            
            return {
                'access_token': access_token,
                'refresh_token': None,  # Don't create new refresh token
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'roles': user.roles
                }
            }
            
        except Exception as e:
            return {'error': str(e), 'code': 'refresh_failed'}, 401 