import json
from six.moves.urllib.request import urlopen
from functools import wraps
from flask_oauth2_validation import OAuth2Decorator

from flask import Flask, request, jsonify
from flask_cors import cross_origin
from jose import jwt

from server import environment,session
import os
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = session.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)

    parts = auth.get("access_token",None).split()
    print(parts[0])
    # if parts[0].lower() != "bearer":
    #     raise AuthError({"code": "invalid_header",
    #                     "description":
    #                         "Authorization header must start with"
    #                         " Bearer"}, 401)
    # elif len(parts) == 1:
    #     raise AuthError({"code": "invalid_header",
    #                     "description": "Token not found"}, 401)
    # elif len(parts) > 2:
    #     raise AuthError({"code": "invalid_header",
    #                     "description":
    #                         "Authorization header must be"
    #                         " Bearer token"}, 401)

    token = parts[0]
    return token

def requires_auth(f):
    """Determines if the Access Token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                "description": "token is expired"}, 401)
            except jwt.JWTClaimsError:
                raise AuthError({"code": "invalid_claims",
                                "description":
                                    "incorrect claims,"
                                    "please check the audience and issuer"}, 401)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                "description":
                                    "Unable to parse authentication"
                                    " token."}, 401)

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                        "description": "Unable to find appropriate key"}, 401)
    return decorated