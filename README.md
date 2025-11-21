# Organization App

The `organization` module owns the multi-level hierarchy that everything else hangs off of
(council → district → etc.).

## Responsibilities

- `Organization` model with name/slug/address mixins and support for nested hierarchies.
- Admin/CRUD views that allow browsing, creating, updating, and deleting organizations.
- Serializers, forms, and tables used by reports and the API.
- Context helpers for resolving the current organization inside other apps.

## Highlights

- Implements reusable queryset helpers for fetching descendants or ancestors.
- Provides DRF viewsets so portals can query organizations without custom wiring.
- Enforces constraints like unique slug per organization tree.

## Tests

```bash
python manage.py test organization
```

Add tests here when you extend the organizational hierarchy logic or introduce new API endpoints.
