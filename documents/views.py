from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, ListView

from inventory.models import JewelryItem

from .forms import DocumentForm
from .models import Document


class OwnedItemMixin(LoginRequiredMixin):
    def get_item(self):
        return get_object_or_404(JewelryItem, pk=self.kwargs["item_id"], user=self.request.user)


class DocumentListView(OwnedItemMixin, ListView):
    template_name = "documents/document_list.html"
    context_object_name = "documents"

    def get_queryset(self):
        self.item = self.get_item()
        return self.item.documents.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item"] = self.item
        return context


class DocumentCreateView(OwnedItemMixin, CreateView):
    model = Document
    form_class = DocumentForm
    template_name = "documents/document_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.item = self.get_item()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.item = self.item
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("documents:list", kwargs={"item_id": self.item.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item"] = self.item
        return context


class DocumentDeleteView(LoginRequiredMixin, DeleteView):
    model = Document
    template_name = "documents/document_confirm_delete.html"

    def get_queryset(self):
        return Document.objects.filter(item__user=self.request.user).select_related("item")

    def get_success_url(self):
        return reverse("documents:list", kwargs={"item_id": self.object.item.pk})
