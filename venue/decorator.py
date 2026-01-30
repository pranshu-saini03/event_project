from functools import wraps

from django.http import JsonResponse
from accounts.models import OwnerPermission


def owner_permission_required(perm_type):

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if request.role == 'admin':
                return view_func(request, *args, **kwargs)

            if request.role == 'owner':

                perm = (
                    OwnerPermission.objects
                    .select_related("permission")
                    .filter(owner_id=request.user_id)
                    .first()
                )

                if not perm:
                    return JsonResponse(
                        {'error': 'No permission assigned'},
                        status=403
                    )

                if perm_type == "create" and not perm.permission.create:
                    return JsonResponse(
                        {'error': 'Create permission denied'},
                        status=403
                    )

                if perm_type == "update" and not perm.permission.update:
                    return JsonResponse(
                        {'error': 'Update permission denied'},
                        status=403
                    )

                if perm_type == "delete" and not perm.permission.delete:
                    return JsonResponse(
                        {'error': 'Delete permission denied'},
                        status=403
                    )

            else:
                return JsonResponse(
                    {'error': 'Permission denied'},
                    status=403
                )

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
