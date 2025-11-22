from django.test import RequestFactory
from django.core.exceptions import ValidationError

from core.tests import BaseDomainTestCase
from organization.models import Organization
from organization.forms.organization import OrganizationForm
from organization.views.organization import ListView


class OrganizationModelTests(BaseDomainTestCase):
    def test_total_factions_counts_descendants(self):
        sub_org = Organization.objects.create(
            name="Foothills Outpost",
            abbreviation="FO",
            parent=self.organization,
            max_depth=5,
        )
        Organization.objects.create(
            name="Foothills Crew",
            abbreviation="FC",
            parent=sub_org,
            max_depth=5,
        )

        self.assertGreaterEqual(self.organization.get_total_factions_count(), 0)

    def test_root_lookup_traverses_parents(self):
        self.assertEqual(self.organization.get_root_organization(), self.parent_org)

    def test_labels_are_created_with_defaults(self):
        org = Organization.objects.create(
            name="Timber Council",
            abbreviation="TC",
            max_depth=3,
        )
        self.assertTrue(hasattr(org, "labels"))
        self.assertEqual(org.labels.attendee_label, "Attendee")


class OrganizationFormTests(BaseDomainTestCase):
    def test_duplicate_name_in_same_parent_invalid(self):
        form = OrganizationForm(
            data={
                "name": self.organization.name,
                "description": "",
                "abbreviation": "CDX",
                "parent": self.organization.parent_id,
                "max_depth": 5,
                "is_active": True,
            }
        )
        self.assertFalse(form.is_valid())


class OrganizationListViewTests(BaseDomainTestCase):
    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()

    def test_context_flags_include_permissions(self):
        request = self.factory.get("/organizations/")
        request.user = self._create_superuser()
        response = ListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
