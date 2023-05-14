from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


STATUS = ((0, "Draft"), (1, "Published"))


class Blog(models.Model):
    """
    Models to create blog posts
    """

    title = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    content = models.TextField()
    image = models.ImageField("image", default="placeholder")
    excerpt = models.TextField(blank=True)
    created_on = models.DateField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name="blog_likes", blank=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()
