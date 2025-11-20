from django.test import TestCase

from core.tests import BaseDomainTestCase
from organization.models import Organization
from faction.models import Faction


class OrganizationModelTests(BaseDomainTestCase):
    def test_total_factions_counts_descendants(self):
        sub_org = Organization.objects.create(
            name="Foothills Outpost",
            abbreviation="FO",
            parent=self.organization,
            max_depth=5,
        )
        Faction.objects.create(name="Foothills Crew", organization=sub_org)

        self.assertEqual(self.organization.get_total_factions_count(), 2)

    def test_root_lookup_traverses_parents(self):
        self.assertEqual(self.organization.get_root_organization(), self.parent_org)
