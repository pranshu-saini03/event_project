from django.http import JsonResponse

from eventproject.utils.jwt_utils import decode_jwt


EXEMPT_URLS = [
    "/admin/",
    "/auth/login/",
    "/auth/register/",
    "/auth/logout/",
]


class JWTAuthenticationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        for url in EXEMPT_URLS:
            if request.path.startswith(url):
                return self.get_response(request)

        auth = request.headers.get('Authorization')

        if not auth:
            return JsonResponse(
                {'error': 'Authorization header missing'},
                status=401
            )

        try:
            token = auth.split(' ')[1]
        except IndexError:
            return JsonResponse(
                {'error': 'Invalid Authorization header format'},
                status=401
            )

        payload = decode_jwt(token)

        if not payload:
            return JsonResponse(
                {'error': 'Invalid or expired token'},
                status=401
            )

        request.user_id = payload.get('user_id')
        request.role = payload.get('role')

        return self.get_response(request)
