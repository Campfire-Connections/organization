# organization/context_processors.py

from django.core.cache import cache

from .models.organization import OrganizationLabels


def organization_labels(request):
    if not request.user.is_authenticated:
        print("User not authenticated")
        return {}

    cache_key = f"organization_labels_{request.user.id}"
    labels = cache.get(cache_key)

    if labels is None:
        labels = fetch_labels(request)
        cache.set(cache_key, labels, timeout=3600)  # Cache for 1 hour

    return {"organization_labels": labels}


def fetch_labels(request):

    user_profile = None
    if hasattr(request.user, "attendeeprofile_profile"):
        user_profile = request.user.attendeeprofile_profile
    elif hasattr(request.user, "leaderprofile_profile"):
        user_profile = request.user.leaderprofile_profile
    elif hasattr(request.user, "facultyprofile_profile"):
        user_profile = request.user.facultyprofile_profile

    if not user_profile:
        print("No profile found for user")
        return {}

    # Default labels
    labels = {
        "attendee_label": "Attendee",
        "facility_label": "Facility",
        "faction_label": "Faction",
        "sub_faction_label": "Sub-Faction",
        "faculty_label": "Faculty",
        "leader_label": "Leader",
        "faculty_quarters_label": "Faculty Quarters",
        "faction_quarters_label": "Faction Quarters",
        "leader_quarters_label": "Leader Quarters",
        "attendee_quarters_label": "Attendee Quarters",
        "course_label": "Course",
        "facility_enrollment_label": "Facility Enrollment",
        "faction_enrollment_label": "Faction Enrollment",
        "leader_enrollment_label": "Leader Enrollment",
        "attendee_enrollment_label": "Attendee Enrollment",
        "attendee_class_enrollment_label": "Attendee Class Enrollment",
        "week_label": "Week",
        "period_label": "Period",
    }

    # Fetch labels from root organization or use defaults
    organization = user_profile.organization.get_root_organization()
    if not organization:
        return {labels}

    organization_labels = (
        organization.labels if hasattr(organization, "labels") else None
    )

    if organization_labels:
        labels.update(
            {
                key: getattr(organization_labels, key, default)
                for key, default in labels.items()
            }
        )

    return labels
