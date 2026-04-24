from django.urls import path

from .views import DocumentCreateView, DocumentDeleteView, DocumentListView

app_name = "documents"

urlpatterns = [
    path("<uuid:item_id>/documents/", DocumentListView.as_view(), name="list"),
    path("<uuid:item_id>/documents/upload/", DocumentCreateView.as_view(), name="create"),
    path("manage/<uuid:pk>/delete/", DocumentDeleteView.as_view(), name="delete"),
]
