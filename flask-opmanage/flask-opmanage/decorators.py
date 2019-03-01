from flask import session,abort
from functools import wraps
def permission_required(permission):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args,**kwargs):
            if permission in session['permissons']:
                return func(*args,**kwargs)
            else:
                abort(403)
        return decorated_function
    return decorator



