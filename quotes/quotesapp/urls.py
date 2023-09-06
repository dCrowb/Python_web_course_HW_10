from django.urls import path, include
from . import views


app_name = 'quotesapp'

urlpatterns = [
    path("", views.main, name="root"),
    path("<int:page>", views.main, name="root_paginate"),
    path("description/<int:quote_id>/", views.about, name="description"),
    path("tags/<str:tag_name>", views.authors_by_tags, name="tags"),
    path('author/add/', views.AuthorView.as_view(), name='add_author'),
    path('quote/add/', views.QuoteView.as_view(), name='add_quote'),
]