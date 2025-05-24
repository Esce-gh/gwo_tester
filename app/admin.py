import csv
import json
import os

from django.contrib import admin, messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.translation import gettext_lazy as _

from app.forms import AdminExportForm, PageForm, PageSetForm
from app.models import Service, Rating, Page, CriteriaPageNumber, CriteriaHeaderFooter, CriteriaObjectDetection, \
    CriteriaOCR, CriteriaImageDetection, PageSetItem, PageSet, PageTypes, CriteriaObjectGroups
from app.utils import get_criteria_model

admin.site.register(Service)
admin.site.register(CriteriaPageNumber)
admin.site.register(CriteriaHeaderFooter)
admin.site.register(CriteriaObjectDetection)
admin.site.register(CriteriaImageDetection)
admin.site.register(CriteriaOCR)
admin.site.register(CriteriaObjectGroups)
admin.site.register(PageSet)
admin.site.register(PageSetItem)


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    change_list_template = "admin/app/page/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload/', self.admin_site.admin_view(self.upload_pages), name='upload-pages'),
        ]
        return custom_urls + urls

    def render_form(self, request, form, errors):
        context = dict(
            self.admin_site.each_context(request),
            form=form,
            title=_('Add pages'),
            errors=errors,
        )
        return TemplateResponse(request, "admin/app/page/upload_pages_form.html", context)

    def upload_pages(self, request):
        if request.method == "GET":
            return self.render_form(request, PageForm(), None)

        page_count = 0
        images = request.FILES.getlist("images")
        image_dict = {}
        for i in images:
            image_dict[os.path.splitext(i.name)[0]] = i

        data = json.load(request.FILES.get("data"))
        pages = []
        for d in data:
            if image_dict.get(d['filename']) is None:
                continue

            sections = []
            for s in d.get('sections', []):
                section_form = PageForm(
                    {'service': request.POST.get('service'), 'execution_time': None,
                     'text': s.get('text'), 'type': PageTypes.SECTION}, files={'image': image_dict.get(s['filename'])})
                if section_form.is_valid() is False:
                    return self.render_form(request, section_form, section_form.errors)
                section = section_form.save(commit=False)
                sections.append(section)
                page_count += 1

            if sections:
                page_form = PageSetForm({'execution_time': d.get('execution_time')},
                                        files={'image': image_dict[d['filename']]})
            else:
                page_form = PageForm(
                    {'service': request.POST.get('service'), 'execution_time': d.get('execution_time'),
                     'type': PageTypes.FULL}, files={'image': image_dict[d['filename']]})
            if page_form.is_valid() is False:
                return self.render_form(request, page_form, page_form.errors)
            page = page_form.save(commit=False)
            pages.append({'page': page, 'sections': sections})
            page_count += 1
        Page.objects.save_pages(pages)
        messages.success(request, _("Added {page_count} pages/page sets.").format(page_count=page_count))
        return redirect("admin:app_page_changelist")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    change_list_template = "admin/app/rating/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export/', self.admin_site.admin_view(self.export_csv), name='rating-export-csv'),
        ]
        return custom_urls + urls

    def export_csv(self, request):
        form = AdminExportForm(request.GET or None)

        if form.is_valid() is False:
            context = dict(
                self.admin_site.each_context(request),
                form=form,
                title=_('Export CSV'),
            )
            return TemplateResponse(request, "admin/app/rating/export_csv_form.html", context)

        criteria_model = get_criteria_model(form.cleaned_data['service'].criteria)
        queryset = criteria_model.objects.get_all_ratings()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="export_{form.cleaned_data['service'].name}.csv"'
        fields_criteria = [field.name for field in criteria_model._meta.fields]
        fields = fields_criteria + ['created_at', 'image', 'execution_time', 'type', 'pageset_execution_time',
                                    'pageset_image']
        writer = csv.writer(response)
        writer.writerow(fields)
        for obj in queryset:
            rating = obj.rating
            page = rating.page
            row = [rating.created_at, page.image, page.execution_time, page.type]
            pagesetitems = list(page.pagesetitem_set.all()) if page.type == PageTypes.SECTION else []
            for p in pagesetitems:
                row += [getattr(p.pageset, 'execution_time', ''), getattr(p.pageset, 'image', '')]
            writer.writerow([getattr(obj, field) for field in fields_criteria] + row)

        return response
