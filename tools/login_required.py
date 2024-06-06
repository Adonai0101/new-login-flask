from functools import wraps
from flask import session, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user") is None:
            return redirect(url_for("index"))  # Redirige al usuario a la página de inicio de sesión
        return f(*args, **kwargs)
    return decorated_function
