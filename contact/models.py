from django.db import models


class Contact(models.Model):
    """
    class for contact model
    """
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.fname
