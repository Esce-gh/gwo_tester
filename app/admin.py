from django.contrib import admin

from app.models import Service, Rating, Page, CriteriaPageNumber

admin.site.register(Service)
admin.site.register(Page)
admin.site.register(Rating)
admin.site.register(CriteriaPageNumber)
