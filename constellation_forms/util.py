from functools import wraps
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from .models import ApiKey


def api_key_required():
    def deny(request):
        raise PermissionDenied

    def decorator(view_function):
        @wraps(view_function)
        def _inner(request, *args, **kwargs):
            if "HTTP_X_AUTHORIZATION" not in request.META:
                deny(request)

            # X-AUTHORIZATION: user api_key
            authorization = request.META["HTTP_X_AUTHORIZATION"]
            user = authorization.split(" ", 1)[0]
            key = authorization.split(" ", 1)[1]

            if not User.objects.filter(username=user).exists():
                deny(request)

            user_object = User.objects.get(username=user)

            if not ApiKey.objects.filter(user=user_object).exists():
                deny(request)

            api_key = ApiKey.objects.get(user=user_object).key

            if len(api_key) != len(key):
                deny(request)
            result = True
            for x, y in zip(api_key, key):
                if x != y:
                    result = False

            if not result:
                deny(request)

            return view_function(request, *args, **kwargs)

        return _inner
    return decorator
