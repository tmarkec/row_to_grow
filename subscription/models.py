from django.db import models
from django.utils import timezone


# Create your models here.
class Subscription(models.Model):
    """
    Subscription on newsletter
    """

    email = models.EmailField()
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email
