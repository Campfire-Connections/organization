# organization/views/organization.py

from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from core.views.base import (
    BaseTableListView,
    BaseListView,
    BaseCreateView,
    BaseUpdateView,
    BaseDeleteView,
    BaseDetailView,
    BaseIndexByFilterTableView,
    BaseSlugOrPkObjectMixin,
)
from core.mixins.views import LoginRequiredMixin, PermissionRequiredMixin
from core.mixins.models import SoftDeleteMixin

from ..models.organization import Organization
from ..forms.organization import OrganizationForm
from ..serializers import OrganizationSerializer
from ..tables.organization import OrganizationTable


class ListView(LoginRequiredMixin, BaseTableListView):
    """
    Table-based list of all organizations.
    Adds can_edit / can_delete flags to the context based on user perms.
    """

    model = Organization
    table_class = OrganizationTable
    template_name = "organization/list.html"
    context_object_name = "organizations"

    def get_queryset(self):
        return Organization.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["can_edit"] = user.has_perm("organization.change_organization")
        context["can_delete"] = user.has_perm("organization.delete_organization")
        return context


class RootListView(LoginRequiredMixin, BaseListView):
    """
    List only root organizations (parent is null).
    """

    model = Organization
    template_name = "organization/index.html"
    context_object_name = "organizations"

    def get_queryset(self):
        return Organization.objects.filter(parent__isnull=True)


class DetailView(LoginRequiredMixin, BaseSlugOrPkObjectMixin, BaseDetailView):
    """
    Detail view that can resolve either:
      - organization_id (pk)
      - organization_slug (slug)
    """

    model = Organization
    template_name = "organization/show.html"
    context_object_name = "organization"
    object_pk_kwarg = "organization_id"
    object_slug_kwarg = "organization_slug"


class ListByParentView(LoginRequiredMixin, BaseIndexByFilterTableView):
    """
    List of organizations filtered by parent org (pk or slug).
    """

    model = Organization
    template_name = "organization/index.html"
    context_object_name = "organizations"

    lookup_keys = ["organization_id", "organization_slug"]
    filter_model = Organization
    filter_field = "parent"
    context_object_name_for_filter = "parent_org"
    table_class = OrganizationTable


class CreateView(LoginRequiredMixin, BaseCreateView):
    """
    Create a new organization; tie created_by to the current user.
    """

    model = Organization
    form_class = OrganizationForm
    template_name = "organization/form.html"
    success_message = "Organization created successfully!"
    success_url = reverse_lazy("organization_index")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class SubOrganizationCreateView(LoginRequiredMixin, BaseCreateView):
    """
    Create a sub-organization under an existing parent (by slug).
    """

    model = Organization
    form_class = OrganizationForm
    template_name = "organization/form.html"
    success_message = "Sub-Organization created successfully!"

    def get_parent_organization(self):
        organization_slug = self.kwargs.get("organization_slug")
        return get_object_or_404(Organization, slug=organization_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["parent"] = self.get_parent_organization()
        return context

    def form_valid(self, form):
        parent = self.get_parent_organization()
        form.instance.parent = parent
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "organization_show",
            kwargs={"organization_slug": self.kwargs["organization_slug"]},
        )


class UpdateView(LoginRequiredMixin, PermissionRequiredMixin, BaseUpdateView):
    """
    Update an organization (requires change_organization permission).
    """

    model = Organization
    form_class = OrganizationForm
    template_name = "organization/form.html"
    permission_required = "organization.change_organization"
    success_message = "Organization updated successfully!"
    success_url = reverse_lazy("organization_list")

    # Use the BaseUpdateView's ActionContextMixin
    action = "Edit"


class DeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SoftDeleteMixin,
    BaseDeleteView,
):
    """
    Soft-delete an organization (requires delete_organization permission).
    """

    model = Organization
    template_name = "organization/confirm_delete.html"
    permission_required = "organization.delete_organization"
    success_message = "Organization deleted successfully!"
    success_url = reverse_lazy("organization_list")

    action = "Delete"


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
