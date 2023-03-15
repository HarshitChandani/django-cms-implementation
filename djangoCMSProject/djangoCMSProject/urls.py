from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("auth/", include("authentication.urls")),
    path('', views.viewPage, {'slug': ''}, name="pages-root"),
    path("<slug:slug>", views.viewPage, name="pages-details-by-slug"),
    path("add-page-form/", views.AddPageForm, name="add-page-form"),
    path("add-page/", views.handleAddPageRequest, name="handleAddPageRequest"),
]
