import django_filters
from ocr.models import Document


class DocumentFilter(django_filters.FilterSet):
    class Meta:
        model = Document
        fields = [
            'status',
        ]