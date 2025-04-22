from django.contrib.auth.models import User
from django.db import models


class Service(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Page(models.Model):
    service = models.ForeignKey(Service, on_delete=models.RESTRICT)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.image.name

class Rating(models.Model):
    page = models.ForeignKey(Page, on_delete=models.RESTRICT)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    is_ok = models.BooleanField()
    comment = models.TextField()

    def __str__(self):
        return f"Rating of {self.page} by {self.user}"
