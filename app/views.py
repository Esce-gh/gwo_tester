import json
import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponseForbidden, HttpResponseNotFound, Http404, HttpResponseServerError
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView, ListView

from app.forms import PageForm, PageSetForm
from app.models import Page, Service, Rating, PageTypes
from app.utils import get_form_class, get_criteria_model


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "app/index.html"


@login_required(login_url='login')
@require_http_methods(['GET', 'POST'])
def create_pages_view(request):
    if request.user.is_superuser is False:
        return redirect("app:index")

    if request.method == "GET":
        return render(request, "app/create_pages.html", {"form": PageForm()})

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
                 'text': s.get('text'), 'type': PageTypes.SECTION}, files={'image': image_dict[s['filename']]})
            if section_form.is_valid() is False:
                return render(request, 'app/create_pages.html', {'form': section_form, 'errors': section_form.errors})
            section = section_form.save(commit=False)
            sections.append(section)

        if sections:
            page_form = PageSetForm({'execution_time': d.get('execution_time')},
                                    files={'image': image_dict[d['filename']]})
        else:
            page_form = PageForm(
                {'service': request.POST.get('service'), 'execution_time': d.get('execution_time'),
                 'type': PageTypes.FULL}, files={'image': image_dict[d['filename']]})
        if page_form.is_valid() is False:
            return render(request, "app/create_pages.html", {"form": page_form, 'errors': page_form.errors})
        page = page_form.save(commit=False)
        pages.append({'page': page, 'sections': sections})
    Page.objects.save_pages(pages)
    return redirect("app:index")


class ServiceListView(LoginRequiredMixin, ListView):
    model = Service
    template_name = "app/service_list.html"
    context_object_name = "services"


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def rate_service_view(request, service_id):
    if request.method == "GET":
        page = Page.objects.get_new_page(request.user, service_id).first()
        criteria_form = get_form_class(page.service.criteria) if page else None
        return render(request, "app/service_rate.html",
                      {"criteria_form": criteria_form, "page": page, 'service_id': service_id})

    try:
        page = Page.objects.get_page(request.POST.get('page_id'))
    except Page.DoesNotExist:
        raise Http404("Page does not exist")

    criteria_form = get_form_class(page.service.criteria)(request.POST)
    if criteria_form.is_valid() is False:
        page = Page.objects.get_new_page(request.user, service_id).first()
        return render(request, "app/service_rate.html",
                      {"criteria_form": criteria_form, "page": page, 'service_id': service_id,
                       "errors": criteria_form.errors})

    criteria = criteria_form.save(commit=False)
    try:
        Rating.objects.save_rating(page, request.user, criteria)
    except IntegrityError:
        return HttpResponseServerError()
    return redirect("app:services-rate", service_id=service_id)


class UserServiceRatingsListView(LoginRequiredMixin, ListView):
    template_name = "app/user_service_ratings.html"
    model = Rating
    context_object_name = "ratings"
    paginate_by = 9

    def get_queryset(self):
        return Rating.objects.get_ratings(self.request.user, self.kwargs['service_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = get_object_or_404(Service, id=self.kwargs['service_id'])
        return context


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def rate_service_edit_view(request, user_id, rating_id):
    if user_id != request.user.id:
        return HttpResponseForbidden()

    try:
        rating = Rating.objects.get_rating(user_id, rating_id)
        criteria = get_criteria_model(rating.criteria).objects.get(rating=rating)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    if request.method == "GET":
        criteria_form = get_form_class(rating.criteria)(instance=criteria)
        return render(request, "app/service_rate.html",
                      {'criteria_form': criteria_form, 'page': rating.page, 'service_id': rating.page.service_id})

    criteria_form = get_form_class(rating.criteria)(request.POST, instance=criteria)
    if criteria_form.is_valid() is False:
        return render(request, "app/service_rate.html",
                      {'criteria_form': criteria_form, "page": rating.page,
                       'service_id': rating.page.service_idm, "errors": criteria_form.errors})

    try:
        Rating.objects.update_rating(rating, criteria)
    except IntegrityError:
        return HttpResponseServerError()
    return redirect("app:user-service-ratings", service_id=rating.page.service_id, user_id=user_id)


def signup(request):
    if request.user.is_authenticated:
        return redirect("app:index")
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app:index')
    else:
        form = UserCreationForm()
    return render(request, 'app/signup.html', {'form': form})
