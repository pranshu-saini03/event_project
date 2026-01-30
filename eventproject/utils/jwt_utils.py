import datetime
import jwt

from django.conf import settings


def generate_jwt(user_id, role):

    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1),
        'iat': datetime.datetime.now(datetime.UTC),
    }

    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm='HS256'
    )

    return token


def decode_jwt(token):

    try:
        decoded = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=['HS256']
        )
        return decoded

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None
