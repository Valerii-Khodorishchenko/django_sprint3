from django.contrib.auth import get_user_model
from django.db import models


class PublicationModel(models.Model):
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Post(PublicationModel):
    title = models.CharField(max_length=256)
    text = models.TextField()
    pub_date = models.DateTimeField()
    autor = models.ForeignKey(
        'User',
        on_delete=models.CASCADE
    )
    location = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        pass


class Category(PublicationModel):
    title = models.CharField(max_length=256)
    description = models.TextField()
    slug = models.SlugField(unique=True)

    class Meta:
        pass


class Location(PublicationModel):
    name = models.CharField(max_length=256)

    class Meta:
        pass


User = get_user_model()
