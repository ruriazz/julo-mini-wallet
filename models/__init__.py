from django.db.models import Manager as __Manager
from django.db.models.query import QuerySet


class BaseModelManager(__Manager):
    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        if hasattr(self.model, 'deleted_at'):
            queryset = queryset.filter(deleted_at__isnull=True)
        return queryset