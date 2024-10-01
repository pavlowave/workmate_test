import pytest
from rest_framework import status
from rest_framework.test import APIClient
from pets.models import Kitten, Breed, Rating
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpass')

@pytest.fixture
def token(user, api_client):
    response = api_client.post('/api/token/', {'username': 'testuser', 'password': 'testpass'})
    return response.data['access']

@pytest.fixture
def authenticated_client(user, api_client, token):
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    return api_client

@pytest.fixture
def breed():
    return Breed.objects.create(name='Persian')

@pytest.fixture
def kitten(breed, user):
    return Kitten.objects.create(
        owner=user,
        breed=breed,
        color='black',
        age_months=3,
        description='A cute black kitten'
    )

@pytest.mark.django_db
class TestBreedViewSet:
    def test_list_breeds(self, api_client, breed):
        response = api_client.get('/api/breeds/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['name'] == breed.name

@pytest.mark.django_db
class TestKittenViewSet:
    def test_create_kitten(self, authenticated_client, breed):
        response = authenticated_client.post('/api/kittens/', {
            'breed': breed.id,
            'color': 'white',
            'age_months': 2,
            'description': 'A fluffy white kitten'
        })
        assert response.status_code == status.HTTP_201_CREATED
        kitten_created = Kitten.objects.get(color='white')
        assert kitten_created.breed == breed
        assert kitten_created.age_months == 2
        assert kitten_created.description == 'A fluffy white kitten'

    def test_update_kitten(self, authenticated_client, kitten):
        response = authenticated_client.patch(f'/api/kittens/{kitten.id}/', {
            'color': 'gray',
            'age_months': 4,
            'description': 'A cute gray kitten'
        })
        assert response.status_code == status.HTTP_200_OK
        kitten.refresh_from_db()
        assert kitten.color == 'gray'

    def test_destroy_kitten(self, authenticated_client, kitten):
        response = authenticated_client.delete(f'/api/kittens/{kitten.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Kitten.objects.filter(id=kitten.id).exists()

    def test_by_color(self, authenticated_client, kitten):
        response = authenticated_client.get('/api/kittens/by-color/?color=black')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_by_breed(self, authenticated_client, breed, user):
        Kitten.objects.create(
        owner=user,
        breed=breed,
        color='black',
        age_months=3,
        description='A cute black kitten'
        )
        response = authenticated_client.get(f'/api/kittens/by-breed/?breed_id={breed.id}')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0  

@pytest.mark.django_db
class TestRatingViewSet:
    def test_create_rating(self, authenticated_client, kitten):
        response = authenticated_client.post('/api/ratings/', {
            'kitten': kitten.id,
            'score': 5
        })
        assert response.status_code == status.HTTP_201_CREATED
        assert Rating.objects.filter(kitten=kitten).exists()

    def test_create_rating_invalid_kitten(self, authenticated_client):
        response = authenticated_client.post('/api/ratings/', {
            'kitten': 999,  # несуществующий ID
            'score': 5
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
