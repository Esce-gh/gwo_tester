from django.contrib import admin

from app.models import Service, Rating, Page, CriteriaPageNumber, CriteriaHeaderFooter, CriteriaObjectDetection, \
    CriteriaOCR, CriteriaImageDetection, PageSetItem, PageSet

admin.site.register(Service)
admin.site.register(Page)
admin.site.register(Rating)
admin.site.register(CriteriaPageNumber)
admin.site.register(CriteriaHeaderFooter)
admin.site.register(CriteriaObjectDetection)
admin.site.register(CriteriaImageDetection)
admin.site.register(CriteriaOCR)
admin.site.register(PageSet)
admin.site.register(PageSetItem)
