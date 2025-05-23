from django.urls import path
from . import views

app_name = 'app'
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("accounts/signup/", views.signup, name="signup"),
    path("services/", views.ServiceListView.as_view(), name="services-list"),
    path("services/<int:service_id>/", views.rate_service_view, name="services-rate"),
    path("users/<int:user_id>/ratings/services/<int:service_id>/", views.UserServiceRatingsListView.as_view(), name="user-service-ratings"),
    path("users/<int:user_id>/ratings/<int:rating_id>/", views.rate_service_edit_view, name="user-rating-edit"),
]