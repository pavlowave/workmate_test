from django.db import models
from django.contrib.auth.models import User


class Breed(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Kitten(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    age_months = models.PositiveIntegerField()
    description = models.TextField()

    def __str__(self):
        return f"{self.color} kitten, {self.age_months} months old"

class Rating(models.Model):
    kitten = models.ForeignKey(Kitten, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Оценка

    class Meta:
        unique_together = ('kitten', 'user')  # Один пользователь может оценить котенка только один раз

    def __str__(self):
        return f"{self.user.username} rated {self.kitten} with score {self.score}"


class UserToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='token')
    token = models.TextField()

    def __str__(self):
        return f"Token for {self.user.username}"