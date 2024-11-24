# organization/views/organization.py

from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView as _ListView,
    DetailView as _DetailView,
    CreateView as _CreateView,
    UpdateView as _UpdateView,
    DeleteView as _DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django_tables2 import SingleTableView

from core.mixins.forms import SuccessMessageMixin, FormValidMixin, ErrorMessageMixin
from core.mixins.models import SoftDeleteMixin

from ..models.organization import Organization
from ..forms.organization import OrganizationForm
from ..serializers import OrganizationSerializer
from ..tables.organization import OrganizationTable


class ListView(LoginRequiredMixin, SingleTableView):
    model = Organization
    table_class = OrganizationTable
    template_name = "organization/list.html"
    context_object_name = "organizations"

    def get_queryset(self):
        return Organization.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_edit"] = self.request.user.has_perm(
            "organization.change_organization"
        )
        context["can_delete"] = self.request.user.has_perm(
            "organization.delete_organization"
        )
        return context


class RootListView(LoginRequiredMixin, _ListView):
    model = Organization
    template_name = "organization/index.html"
    context_object_name = "organizations"

    def get_queryset(self):
        return Organization.objects.filter(parent__isnull=True)


class DetailView(LoginRequiredMixin, _DetailView):
    model = Organization
    template_name = "organization/show.html"
    context_object_name = "organization"

    def get_object(self):
        organization_id = self.kwargs.get("organization_id")
        organization_slug = self.kwargs.get("organization_slug")
        if organization_id:
            return get_object_or_404(Organization, pk=organization_id)
        else:
            return get_object_or_404(Organization, slug=organization_slug)


class ListByParentView(LoginRequiredMixin, _ListView):
    model = Organization
    template_name = "organization/index.html"
    context_object_name = "organizations"

    def get_queryset(self):
        organization_id = self.kwargs.get("organization_id")
        organization_slug = self.kwargs.get("organization_slug")
        if organization_id:
            parent_org = get_object_or_404(Organization, pk=organization_id)
        else:
            parent_org = get_object_or_404(Organization, slug=organization_slug)
        return Organization.objects.filter(parent=parent_org)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        organization_id = self.kwargs.get("organization_id")
        organization_slug = self.kwargs.get("organization_slug")
        if organization_id:
            context["parent_org"] = get_object_or_404(Organization, pk=organization_id)
        else:
            context["parent_org"] = get_object_or_404(
                Organization, slug=organization_slug
            )
        return context


class CreateView(LoginRequiredMixin, SuccessMessageMixin, FormValidMixin, _CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = "organization/form.html"
    success_message = "Organization created successfully!"
    success_url = reverse_lazy("organization_index")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class SubOrganizationCreateView(
    LoginRequiredMixin, SuccessMessageMixin, FormValidMixin, _CreateView
):
    model = Organization
    form_class = OrganizationForm
    template_name = "organization/form.html"
    success_message = "Sub-Organization created successfully!"

    def get_success_url(self):
        return reverse_lazy(
            "organization_show",
            kwargs={"organization_slug": self.kwargs["organization_slug"]},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["parent"] = self.get_parent_organization()
        return context

    def get_parent_organization(self):
        organization_slug = self.kwargs.get("organization_slug")
        return get_object_or_404(Organization, slug=organization_slug)

    def form_valid(self, form):
        parent_organization = self.get_parent_organization()
        form.instance.parent = parent_organization
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class UpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    FormValidMixin,
    _UpdateView,
):
    model = Organization
    form_class = OrganizationForm
    template_name = "organization/form.html"
    permission_required = "organization.change_organization"
    success_message = "Organization updated successfully!"
    success_url = reverse_lazy("organization_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "Edit"
        return context


class DeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SoftDeleteMixin,
    SuccessMessageMixin,
    _DeleteView,
):
    model = Organization
    template_name = "organization/confirm_delete.html"
    permission_required = "organization.delete_organization"
    success_message = "Organization deleted successfully!"
    success_url = reverse_lazy("organization_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "Delete"
        return context
