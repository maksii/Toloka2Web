from flask import request, jsonify, abort, g
from functools import wraps
from flask_login import current_user

def login_or_api_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in
        if not current_user.is_authenticated:
            # If not logged in, check for API key
            api_key = request.headers.get('x_api_key')
            if not api_key or api_key != 'your_api_key_here':  # Validate API key # TBD temporary to allow cron. Will need logic to provision api keys from db, and later on pass to cron
                abort(403, description="Access denied: No valid API key or login session")
        return f(*args, **kwargs)
    return decorated_function