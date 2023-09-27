from asgiref.sync import sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth import get_user_model


class BaseAuthMiddleware(BaseMiddleware):
    user_model = get_user_model()

    async def __call__(self, scope, receive, send):
        scope['user'] = self.get_user()
        return await super().__call__(scope, receive, send)

    @sync_to_async
    def get_user(self):
        try:
            user = User.objects.get(is_superuser=True)
        except self.user_model.DoesNotExist:
            user = AnonymousUser
        except self.user_model.MultipleObjectsReturned:
            user = AnonymousUser

        return user
