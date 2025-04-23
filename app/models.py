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


class RatingManager(models.Manager):
    def get_ratings(self, user, service_id):
        return self.get_queryset().select_related("page").filter(user=user, page__service_id=service_id).order_by("-created_at")

    def get_rating(self, user, rating_id):
        return self.get_queryset().select_related("page").get(id=rating_id, user=user)

class Rating(models.Model):
    page = models.ForeignKey(Page, on_delete=models.RESTRICT)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    is_ok = models.BooleanField()
    comment = models.TextField(blank=True, null=True)

    objects = RatingManager()

    def __str__(self):
        return f"Rating of {self.page} by {self.user}"

    class Meta:
        unique_together = ['page', 'user']
