from flask import session,abort,request,current_app
from flask.ext.login import current_user
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

def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
	if session['permissons']:
	    return func(*args,**kwargs)
        elif request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
	return func(*args, **kwargs)
    return decorated_view
