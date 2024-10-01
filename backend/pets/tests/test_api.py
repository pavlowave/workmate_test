import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from pets.models import Breed, Kitten, Rating
from rest_framework_simplejwt.tokens import AccessToken

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpassword')

@pytest.fixture
def token(user):
    return AccessToken.for_user(user)

@pytest.fixture
def breed(db):
    return Breed.objects.create(name='Сиамская')  

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.mark.django_db
def test_create_kitten(api_client, user, token, breed):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    response = api_client.post(reverse('kitten-list'), {
        'breed': breed.id,
        'color': 'черный',
        'age_months': 12,
        'description': 'Прекрасный котенок'
    })

    assert response.status_code == 201
    assert response.data['breed'] == breed.id

@pytest.mark.django_db
def test_create_rating(api_client, user, token, breed):
    kitten = Kitten.objects.create(owner=user, breed=breed, color='белый', age_months=5, description='Милый котенок')

    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    response = api_client.post(reverse('rating-list'), {
        'kitten': kitten.id,
        'score': 5,
        'user': user.id
    }, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert Rating.objects.count() == 1
    assert Rating.objects.get().score == 5

@pytest.mark.django_db
def test_get_kittens_with_average_rating(api_client, user, token, breed):
    kitten = Kitten.objects.create(owner=user, breed=breed, color='черный', age_months=2, description='Котенок')

    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    api_client.post(reverse('rating-list'), {
        'kitten': kitten.id,
        'score': 4,
        'user': user.id
    }, format='json')

    response = api_client.get(reverse('kitten-list'))

    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]['average_rating'] == 4.0
