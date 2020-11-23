from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.urls import resolve
from login_required.middleware import LoginRequiredMiddleware
User = get_user_model()

BB_PRODUCTS_VIEW_NAME = [
    name
    for name in getattr(settings, 'BB_PRODUCTS_VIEW_NAME', [])
]

POPULATIONS_VIEW_NAME = [
    name
    for name in getattr(settings, 'POPULATIONS_VIEW_NAME', [])
]

IGNORE_VIEW_NAMES = [
    name
    for name in getattr(settings, 'LOGIN_REQUIRED_IGNORE_VIEW_NAMES', [])
]


class MultiDatabaseMiddleware(LoginRequiredMiddleware):

    def process_request(self, request):
        assert hasattr(request, 'user'), (
            'The LoginRequiredMiddleware requires authentication middleware '
            'to be installed. Edit your MIDDLEWARE setting to insert before '
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        )
        path = request.path
        bb_views, pop_views, views = None, None, None
        resolver = resolve(path)

        if not request.user:
            raise PermissionDenied

        if resolver.view_name in BB_PRODUCTS_VIEW_NAME:
            bb_views = True
        if resolver.view_name in POPULATIONS_VIEW_NAME:
            pop_views = True

        if not pop_views and not bb_views:
            if resolver.view_name in IGNORE_VIEW_NAMES:
                views = True
            if views:
                return
            if request.user.is_authenticated and request.user.db_role != 0:
                raise PermissionDenied
            return super().process_request(request)

        if bb_views:
            db_role = [0, 1]
            bb_product_user = User.objects.filter(db_role__in=db_role, username__exact=request.user.username)
            if not bb_product_user:
                raise PermissionDenied
            return

        if pop_views:
            db_role = [0, 2]
            pop_user = User.objects.filter(db_role__in=db_role, username__exact=request.user.username)
            if not pop_user:
                raise PermissionDenied
            return
        return super().process_request(request)
