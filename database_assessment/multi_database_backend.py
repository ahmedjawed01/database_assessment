from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class MultiDatabaseBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        request_path = request.path
        try:
            if request_path == '/admin/login/':
                user = User.objects.get(db_role=0, username=username)
            else:
                if request_path == '/bb-product-login/':
                    db = 1
                elif request_path == '/population-login/':
                    db = 2
                else:
                    db = 0
                user = User.objects.get(db_role=int(db), username=username)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
