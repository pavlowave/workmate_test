from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BreedViewSet, KittenViewSet, RatingViewSet


router = DefaultRouter()
router.register(r'breeds', BreedViewSet)    # Маршруты для пород
router.register(r'kittens', KittenViewSet)  # Маршруты для котят
router.register(r'ratings', RatingViewSet)  # Маршруты для оценок котят


urlpatterns = [
    path('', include(router.urls)),
]