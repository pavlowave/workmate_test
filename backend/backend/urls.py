from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Настройка Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Kitten API",
        default_version='v1',
        description="API для онлайн выставки котят",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Определение переменной urlpatterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # Эндпоинты для JWT аутентификации
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Основные urls приложения
    path('api/', include('pets.urls')),
]