# organization/tables/organization.py

import django_tables2 as tables

from ..models.organization import Organization


class OrganizationTable(tables.Table):
    controls = tables.TemplateColumn(
        template_name="organization/partials/controls.html",
        verbose_name="Actions",
        orderable=False,
    )

    class Meta:
        model = Organization
        template_name = "django_tables2/bootstrap4.html"
        fields = ("name", "description", "abbreviation", "max_depth", "parent")
        attrs = {"class": "table table-striped table-bordered"}
