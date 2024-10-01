from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Kitten, Breed, Rating
from .serializers import KittenSerializer, BreedSerializer, RatingSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.exceptions import PermissionDenied, ValidationError


class BreedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = [permissions.AllowAny]

class KittenViewSet(viewsets.ModelViewSet):
    queryset = Kitten.objects.all()
    serializer_class = KittenSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        # Разрешения для авторизованных пользователей
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            # Для метода list (для всех)
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def get_queryset(self):
        return Kitten.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        kitten = self.get_object()
        if kitten.owner != self.request.user:
            raise PermissionDenied("Вы не можете редактировать этого котенка.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied("Вы не можете удалить этого котенка")
        instance.delete()

    @action(detail=False, methods=['get'], url_path='by-color')
    def by_color(self, request):
        color = request.query_params.get('color', None)
        if color:
            kittens = self.get_queryset().filter(color=color)
            if not kittens.exists():
                return Response({"detail": "Котята с таким цветом не найдены."}, status=404)
            serializer = self.get_serializer(kittens, many=True)
            return Response(serializer.data)
        return Response({"detail": "Цвет не указан."}, status=400)

    @action(detail=False, methods=['get'], url_path='by-breed')
    def by_breed(self, request):
        breed_id = request.query_params.get('breed_id', None)
        if breed_id:
            kittens = self.get_queryset().filter(breed_id=breed_id)
            if not kittens.exists():
                return Response({"detail": "Котята данной породы не найдены."}, status=404)
            serializer = self.get_serializer(kittens, many=True)
            return Response(serializer.data)
        return Response({"detail": "ID породы не указан."}, status=400)

class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Rating.objects.all()

    def perform_create(self, serializer):

        kitten_id = self.request.data.get('kitten')
        if not Kitten.objects.filter(id=kitten_id).exists():
            raise ValidationError({"detail": "Котенок с данным ID не найден."})

        # Привязать рейтинг к пользователю
        serializer.save(user=self.request.user)