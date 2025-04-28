from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, IntegrityError
from django.forms.utils import ErrorDict
from django.http import HttpResponseForbidden, HttpResponseNotFound, Http404, HttpResponseServerError
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView, ListView

from app.forms import PageForm, RatingForm
from app.models import Page, Service, Rating
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
    pages = []
    for image in images:
        form = PageForm(request.POST, files={"image": image})
        if form.is_valid() is False:
            return render(request, "app/create_pages.html", {"form": form, "errors": form.errors})
        page = form.save(commit=False)
        pages.append(page)

    Page.objects.bulk_create(pages)
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
        rating_form = RatingForm(initial={'page_id': getattr(page, 'id', None)})
        return render(request, "app/service_rate.html",
                      {"criteria_form": criteria_form, 'rating_form': rating_form, "page": page})

    try:
        page = Page.objects.get_page(request.POST.get('page_id'))
    except Page.DoesNotExist:
        raise Http404("Page does not exist")

    rating_form = RatingForm(request.POST)
    criteria_form = get_form_class(page.service.criteria)(request.POST)
    if rating_form.is_valid() is False or criteria_form.is_valid() is False:
        page = Page.objects.get_new_page(request.user, service_id).first()
        errors = ErrorDict()
        errors.update(rating_form.errors)
        errors.update(criteria_form.errors)
        return render(request, "app/service_rate.html",
                      {"criteria_form": criteria_form, 'rating_form': rating_form, "page": page, "errors": errors})

    rating = rating_form.save(commit=False)
    rating.page = page
    rating.user = request.user
    rating.criteria = page.service.criteria
    criteria = criteria_form.save(commit=False)
    criteria.rating = rating

    try:
        Rating.objects.save_rating(rating, criteria)
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
        context['service'] = Service.objects.get(pk=self.kwargs['service_id'])
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
        rating_form = RatingForm(instance=rating, initial={'page_id': getattr(rating.page, 'id', None)})
        criteria_form = get_form_class(rating.criteria)(instance=criteria)
        return render(request, "app/service_rate.html",
                      {"rating_form": rating_form, 'criteria_form': criteria_form, 'page': rating.page})

    rating_form = RatingForm(request.POST, instance=rating)
    criteria_form = get_form_class(rating.criteria)(request.POST, instance=criteria)
    if rating_form.is_valid() is False or criteria_form.is_valid() is False:
        errors = ErrorDict()
        errors.update(rating_form.errors)
        errors.update(criteria_form.errors)
        return render(request, "app/service_rate.html",
                      {"rating_form": rating_form, 'criteria_form': criteria_form, "page": rating.page,
                       "errors": errors})

    new_rating = rating_form.save(commit=False)
    new_rating.created_at = timezone.now()

    try:
        Rating.objects.save_rating(new_rating, criteria)
    except IntegrityError:
        return HttpResponseServerError()
    return redirect("app:user-service-ratings", service_id=rating.page.service_id, user_id=user_id)
