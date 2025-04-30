from django.contrib.auth.models import User
from django.db import models, transaction, IntegrityError


class RatingCriteria(models.TextChoices):
    PAGE_NUMBER = 'PN', 'Page Number Criteria'
    HEADER_FOOTER = 'HF', 'Header Footer Criteria'
    OBJECT_DETECTION = 'OD', 'Object Detection Criteria'


class Service(models.Model):
    name = models.CharField(max_length=100)
    criteria = models.CharField(choices=RatingCriteria.choices)

    def __str__(self):
        return self.name


class PageManager(models.Manager):
    def get_new_page(self, user, service_id):
        queryset = (self.get_queryset()
                    .filter(service_id=service_id)
                    .prefetch_related("rating_set")
                    .select_related("service")
                    .exclude(rating__user=user))
        return queryset

    def get_page(self, page_id):
        return self.get_queryset().select_related('service').get(pk=page_id)


class Page(models.Model):
    service = models.ForeignKey(Service, on_delete=models.RESTRICT)
    image = models.ImageField(upload_to='images/')

    objects = PageManager()

    def __str__(self):
        return self.image.name


class RatingManager(models.Manager):
    def get_ratings(self, user, service_id):
        return (self.get_queryset()
                .select_related("page")
                .filter(user=user, page__service_id=service_id)
                .order_by("-created_at"))

    def get_rating(self, user, rating_id):
        return self.get_queryset().select_related("page").get(id=rating_id, user=user)

    def save_rating(self, rating, criteria):
        with transaction.atomic():
            rating.save()
            criteria.save()


class Rating(models.Model):
    page = models.ForeignKey(Page, on_delete=models.RESTRICT)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    criteria = models.CharField(choices=RatingCriteria.choices)

    objects = RatingManager()

    def __str__(self):
        return f"Rating of {self.page} by {self.user}"

    class Meta:
        unique_together = ['page', 'user']


class CriteriaBaseClass(models.Model):
    rating = models.OneToOneField(Rating, on_delete=models.RESTRICT)

    class Meta:
        abstract = True

    def __str__(self):
        return f"Criteria for {self.rating}"


class CriteriaPageNumber(CriteriaBaseClass):
    page_number_visible = models.BooleanField()
    page_number_detected = models.BooleanField()


class CriteriaHeaderFooter(CriteriaBaseClass):
    header_visible = models.BooleanField()
    header_detected = models.BooleanField()
    footer_visible = models.BooleanField()
    footer_detected = models.BooleanField()


class CriteriaObjectDetection(CriteriaBaseClass):
    visible_objects = models.IntegerField()
    detected_objects = models.IntegerField()
