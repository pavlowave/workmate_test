from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserToken

@receiver(post_save, sender=User)
def create_user_token(sender, instance, created, **kwargs):
    if created:
        # Генерируем токен для нового пользователя
        refresh = RefreshToken.for_user(instance)
        UserToken.objects.create(user=instance, token=str(refresh.access_token))
    else:
        # Обновляем токен при изменении пользователя
        user_token = UserToken.objects.get(user=instance)
        refresh = RefreshToken.for_user(instance)
        user_token.token = str(refresh.access_token)
        user_token.save()