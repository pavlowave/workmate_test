from rest_framework import serializers
from .models import Kitten, Breed, Rating

class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ['id', 'name']

class KittenSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    breed_name = serializers.CharField(source='breed.name', read_only=True)

    class Meta:
        model = Kitten
        fields = ['id', 'breed_name', 'color', 'age_months', 'description', 'average_rating']
        read_only_fields = ['owner']

    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings:
            return sum(rating.score for rating in ratings) / ratings.count()
        return None

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['kitten', 'score']