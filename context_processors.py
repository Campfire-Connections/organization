# organization/context_processors.py

import inflect

from django.core.cache import cache

from .models.organization import OrganizationLabels


def organization_labels(request):
    """
    Context processor to provide organization labels in singular and plural forms.
    Includes handling for pluralization exceptions.
    """
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
    """
    Fetches labels for the current user's organization. Includes singular
    and pluralized versions of the labels with exception handling.
    """
    user_profile = None
    if hasattr(request.user, "attendeeprofile_profile"):
        user_profile = request.user.attendeeprofile_profile
    elif hasattr(request.user, "leaderprofile_profile"):
        user_profile = request.user.leaderprofile_profile
    elif hasattr(request.user, "facultyprofile_profile"):
        user_profile = request.user.facultyprofile_profile

    # Default labels
    default_labels = {
        "attendee_label": "Attendee",
        "facility_label": "Facility",
        "faction_label": "Faction",
        "sub_faction_label": "Sub-Faction",
        "faculty_label": "Faculty",
        "leader_label": "Leader",
        "quarters_label": "Quarters",
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
        "department_label": "Department",
    }

    if not user_profile:
        print("No profile found for user")
        return default_labels

    # Plural exceptions
    plural_exceptions = {
        "quarters_label": "Quarters",
        "faculty_label": "Faculty",
    }

    # Fetch organization and its labels
    organization = user_profile.organization.get_root_organization()
    if not organization:
        return add_pluralized_labels(default_labels, plural_exceptions)

    organization_labels = (
        organization.labels if hasattr(organization, "labels") else None
    )

    labels = default_labels.copy()  # Start with default labels
    if organization_labels:
        # Update labels with organization-specific values
        labels.update(
            {
                key: getattr(organization_labels, key, default)
                for key, default in default_labels.items()
            }
        )

    return add_pluralized_labels(labels, plural_exceptions)


def add_pluralized_labels(labels, plural_exceptions):
    """
    Adds pluralized versions of the labels to the dictionary.

    Args:
        labels (dict): A dictionary of singular labels.
        plural_exceptions (dict): A dictionary of labels with predefined plural forms.

    Returns:
        dict: Updated dictionary with pluralized labels.
    """
    inflector = inflect.engine()
    pluralized_labels = {}

    for key, value in labels.items():
        if key in plural_exceptions:
            # Use the exception-defined plural form
            pluralized_labels[f"{key}_plural"] = plural_exceptions[key]
        else:
            # Generate the plural form dynamically
            pluralized_labels[f"{key}_plural"] = inflector.plural(value)

    labels.update(pluralized_labels)
    return labels
