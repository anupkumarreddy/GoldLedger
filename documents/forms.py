from django import forms

from inventory.forms import StyledModelForm

from .models import Document


class DocumentForm(StyledModelForm):
    class Meta:
        model = Document
        fields = ("document_type", "title", "file", "notes")
