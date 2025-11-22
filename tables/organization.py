# organization/tables/organization.py

import django_tables2 as tables

from core.tables.base import BaseTable
from ..models.organization import Organization


class OrganizationTable(BaseTable):
    available_actions = ["show", "edit", "delete"]
    url_namespace = ""  # explicit names below

    class Meta:
        model = Organization
        template_name = "django_tables2/bootstrap4.html"
        fields = ("name", "description", "abbreviation", "max_depth", "parent")
        attrs = {"class": "table table-striped table-bordered"}

    urls = {
        "add": {"name": "organization_new", "kwargs": {}},
        "show": {"name": "organization_show", "kwargs": {"organization_slug": "slug"}},
        "edit": {"name": "organization_edit", "kwargs": {"organization_slug": "slug"}},
        "delete": {
            "name": "organization_delete",
            "kwargs": {"organization_slug": "slug"},
        },
    }
