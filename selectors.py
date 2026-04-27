from django.shortcuts import get_object_or_404

from organization.models.organization import Organization


def organization_queryset():
    return Organization.objects.all()


def root_organizations_queryset():
    return organization_queryset().filter(parent__isnull=True)


def get_organization_by_slug(slug):
    return get_object_or_404(Organization, slug=slug)
