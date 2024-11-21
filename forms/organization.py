# organization/forms/organization.py

from django import forms
from ..models.organization import Organization, OrganizationLabels

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = [
            'name',
            'description',
            'abbreviation',
            'parent',  # Assuming you want to allow setting a parent organization
            'image',
            'max_depth',
            'is_active',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'abbreviation': forms.TextInput(attrs={'class': 'form-control'}),
            'max_depth': forms.NumberInput(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        # Perform any custom validation here if needed.
        return cleaned_data


class OrganizationLabelsForm(forms.ModelForm):
    class Meta:
        model = OrganizationLabels
        fields = [
            'attendee_label',
            'facility_label',
            'faction_label',
            'sub_faction_label',
            'faculty_label',
            'leader_label',
            'faculty_quarters_label',
            'faction_quarters_label',
            'leader_quarters_label',
            'attendee_quarters_label',
            'course_label',
            'facility_enrollment_label',
            'faction_enrollment_label',
            'leader_enrollment_label',
            'attendee_enrollment_label',
            'attendee_class_enrollment_label',
            'week_label',
            'period_label',
        ]
        
