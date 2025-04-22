from django.contrib.auth.models import User
from django.db import models
from django.db.models import Prefetch


class Service(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PageManager(models.Manager):
    def get_new_page(self, user, service_id):
        queryset = self.get_queryset().filter(service_id=service_id).prefetch_related("rating_set").exclude(
            rating__user=user)
        return queryset


class Page(models.Model):
    service = models.ForeignKey(Service, on_delete=models.RESTRICT)
    image = models.ImageField(upload_to='images/')

    objects = PageManager()

    def __str__(self):
        return self.image.name


class Rating(models.Model):
    page = models.ForeignKey(Page, on_delete=models.RESTRICT)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    is_ok = models.BooleanField()
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Rating of {self.page} by {self.user}"
