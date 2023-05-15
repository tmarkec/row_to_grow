from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Count


class Category(models.Model):
    """
    class for categories for products
    """
    class Meta:
        verbose_name_plural = 'Categories'
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    """
    class for products
    """
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    original_price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    rating = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    def averageReview(self):
        reviews = Review.objects.filter(
            product=self, approved=True
            ).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = int(reviews['average'])
        return avg

    def countReview(self):
        reviews = Review.objects.filter(
            product=self, approved=True
            ).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count


class Review(models.Model):
    """
    class for reviews and ratings of the product
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_comment = models.TextField(max_length=120)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(null=True, blank=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Review for {self.product.name}"
