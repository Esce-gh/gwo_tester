from django.urls import path
from . import views

app_name = 'app'
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("pages/", views.create_pages_view, name="create-pages"),
    path("services/", views.ServiceListView.as_view(), name="services-list"),
    path("services/<int:service_id>/", views.rate_service_view, name="services-rate"),
    path("services/<int:service_id>/user-ratings/", views.UserServiceRatingsListView.as_view(), name="user-service-ratings"),
    path("users/<int:user_id>/ratings/<int:rating_id>/", views.rate_service_edit_view, name="user-rating-edit"),
]