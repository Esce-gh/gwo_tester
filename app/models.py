from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import Prefetch
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class RatingCriteria(models.TextChoices):
    PAGE_NUMBER = 'PN', 'Page Number Criteria'
    HEADER_FOOTER = 'HF', 'Header Footer Criteria'
    OBJECT_DETECTION = 'OD', 'Object Detection Criteria'
    IMAGE_DETECTION = 'IMD', 'Image Detection Criteria'
    OCR = 'OCR', 'OCR Criteria'


class PageTypes(models.TextChoices):
    FULL = 'F', 'Full Page'
    SECTION = 'S', 'Page Section'


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

    def save_pages(self, page_data):
        pages = []
        page_sets = []
        page_set_items = []
        for p in page_data:
            if not p.get('sections'):
                pages.append(p['page'])
                continue
            page_sets.append(p['page'])
            for s in p['sections']:
                pages.append(s)
                page_set_items.append(PageSetItem(page=s, pageset=p['page']))
        with transaction.atomic():
            self.bulk_create(pages)
            PageSet.objects.bulk_create(page_sets)
            PageSetItem.objects.bulk_create(page_set_items)


class Page(models.Model):
    service = models.ForeignKey(Service, on_delete=models.RESTRICT, verbose_name=_('Service'))
    image = models.ImageField(upload_to='images/', verbose_name=_('Image'))
    execution_time = models.FloatField(blank=True, null=True, verbose_name=_('Execution Time'))
    text = models.TextField(blank=True, null=True, verbose_name=_('Text'))
    type = models.CharField(choices=PageTypes.choices, default=PageTypes.FULL)

    objects = PageManager()

    def __str__(self):
        return self.image.name


class PageSet(models.Model):
    image = models.ImageField(upload_to='images/', verbose_name=_('Image'))
    execution_time = models.FloatField(blank=True, null=True, verbose_name=_('Execution Time'))

    def __str__(self):
        return self.image.name


class PageSetItem(models.Model):
    pageset = models.ForeignKey(PageSet, on_delete=models.RESTRICT)
    page = models.ForeignKey(Page, on_delete=models.RESTRICT)

    def __str__(self):
        return f'Pageset: {self.pageset} Page: {self.page}'


class RatingManager(models.Manager):
    def get_ratings(self, user, service_id):
        return (self.get_queryset()
                .select_related("page")
                .filter(user=user, page__service_id=service_id)
                .order_by("-created_at"))

    def get_rating(self, user, rating_id):
        return self.get_queryset().select_related("page").get(id=rating_id, user=user)

    def save_rating(self, page, user, criteria):
        rating = Rating(page=page, user=user, criteria=page.service.criteria)
        with transaction.atomic():
            rating.save()
            criteria.rating = rating
            criteria.save()

    def update_rating(self, rating, criteria):
        rating.created_at = timezone.now()
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
        return f"Rating of {self.page} by {self.user_id}"

    class Meta:
        unique_together = ['page', 'user']


class CriteriaManager(models.Manager):
    def get_all_ratings(self):
        queryset = self.get_queryset().all().select_related('rating__page')
        if self.model == CriteriaOCR:
            queryset = queryset.prefetch_related(
                Prefetch('rating__page__pagesetitem_set', queryset=PageSetItem.objects.select_related('pageset')))
        return queryset


class CriteriaBaseClass(models.Model):
    rating = models.OneToOneField(Rating, on_delete=models.RESTRICT)
    comment = models.TextField(blank=True, verbose_name=_('Additional notes'))

    objects = CriteriaManager()

    class Meta:
        abstract = True

    def __str__(self):
        return f"Criteria for {self.rating}"


class CriteriaPageNumber(CriteriaBaseClass):
    page_number_visible = models.BooleanField(verbose_name=_("Is page number visible"))
    page_number_detected = models.BooleanField(verbose_name=_("Is page number detected"))


class CriteriaHeaderFooter(CriteriaBaseClass):
    header_visible = models.BooleanField(verbose_name=_("Is header visible"))
    header_detected = models.BooleanField(verbose_name=_("Is header detected"))
    footer_visible = models.BooleanField(verbose_name=_("Is footer visible"))
    footer_detected = models.BooleanField(verbose_name=_("Is footer detected"))


class CriteriaObjectDetection(CriteriaBaseClass):
    visible_objects = models.IntegerField(verbose_name=_("Visible objects"))
    detected_objects = models.IntegerField(verbose_name=_("Correctly detected objects"))


class CriteriaImageDetection(CriteriaBaseClass):
    visible_images = models.IntegerField(verbose_name=_("Visible images"))
    detected_images = models.IntegerField(verbose_name=_("Correctly detected images"))


class CriteriaOCR(CriteriaBaseClass):
    word_recognition_errors = models.IntegerField(verbose_name=_("Number of misrecognized words"))
