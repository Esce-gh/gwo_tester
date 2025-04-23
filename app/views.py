from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import TemplateView, ListView

from app.forms import PageForm, RatingForm
from app.models import Page, Service, Rating


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "app/index.html"


@login_required(login_url='login')
def create_pages_view(request):
    if request.user.is_superuser is False:
        return redirect("app:index")

    if request.method == "POST":
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

    return render(request, "app/create_pages.html", {"form": PageForm()})


class ServiceListView(LoginRequiredMixin, ListView):
    model = Service
    template_name = "app/service_list.html"
    context_object_name = "services"


@login_required(login_url='login')
def rate_service_view(request, service_id):
    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.page = get_object_or_404(Page, pk=request.POST.get("page_id"))
            rating.user = request.user
            rating.save()
            return redirect("app:services-rate", service_id=service_id)
        page = Page.objects.get_new_page(request.user, service_id).first()
        return render(request, "app/service_rate.html", {"form": form, "page":page, "errors": form.errors})

    page = Page.objects.get_new_page(request.user, service_id).first()
    form = RatingForm(initial={'page_id': getattr(page, 'id', None)})
    return render(request, "app/service_rate.html", {"form": form, "page": page})


class UserServiceRatingsListView(LoginRequiredMixin, ListView):
    template_name = "app/user_service_ratings.html"
    model = Rating
    context_object_name = "ratings"

    def get_queryset(self):
        return Rating.objects.get_ratings(self.request.user, self.kwargs['service_id'])


@login_required(login_url='login')
def rate_service_edit_view(request, user_id, rating_id):
    if user_id != request.user.id:
        return HttpResponseForbidden()
    try:
        rating = Rating.objects.get_rating(user_id, rating_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    if request.method == "POST":
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            new_rating = form.save(commit=False)
            new_rating.created_at = timezone.now()
            new_rating.save()
            return redirect("app:user-service-ratings", service_id=rating.page.service_id, user_id=user_id)
        return render(request, "app/service_rate.html", {"form": form, "page": rating.page, "errors": form.errors})

    form = RatingForm(instance=rating, initial={'page_id': getattr(rating.page, 'id', None)})
    return render(request, "app/service_rate.html", {"form": form, 'page': rating.page})
