from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.adverts.models import Advert
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class CustomUser(AbstractUser):
    """ This class models a marche user
    """
    id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    residence_hall = models.CharField(max_length=12, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    wishlist = models.ManyToManyField(Advert, blank=True, related_name="users")
    profile_picture = models.ImageField(upload_to="profile_pic", default="default.jpg")


#user-review
class Review(models.Model):
    """ This class models a review object
    """
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE, related_name="reviews_created")
    reviewee = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, 
                                    on_delete=models.SET_NULL,
                                    related_name="reviews")
    rating = models.PositiveIntegerField()
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
       unique_together = ("reviewer", "reviewee")


