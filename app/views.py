from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView

from app.forms import PageForm, RatingForm
from app.models import Page, Service


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "app/index.html"


@login_required(login_url='login')
def create_pages_view(request):
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
        return redirect("app:index")  # TODO: change the redirect

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
        return render(request, "app/service_rate.html", {"form": form, "errors": form.errors})

    page = Page.objects.get_new_page(request.user, service_id).first()
    form = RatingForm(initial={'page_id': getattr(page, 'id', None)})
    return render(request, "app/service_rate.html", {"form": form, "page": page})
