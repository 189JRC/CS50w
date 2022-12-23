from django.urls import path

from . import views

urlpatterns = [
    path("index/", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("new_entry/", views.new_entry, name="new_entry"),
    path("error/", views.error, name="error"),
    path("thanks/", views.thanks, name="thanks"),
    path("random/", views.rando, name="rando"),
    path("edit/", views.edit, name="edit"),
    path("save/", views.save, name="save"),
    path("search", views.search, name="search"),
]
