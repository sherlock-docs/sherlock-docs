import django_filters
from .models import Document, PageDocument


class DocumentFilter(django_filters.FilterSet):
    class Meta:
        model = Document
        fields = [
            'status',
        ]


class PageDocumentFilter(django_filters.FilterSet):
    type_id = django_filters.Filter(name='type_id', lookup_expr='exact')
    type_name = django_filters.Filter(name='type__name', lookup_expr='exact')
    text = django_filters.Filter(name='text', lookup_expr='icontains')

    class Meta:
        model = PageDocument
        fields = [
            'type_id',
            'type_name',
            'text',
            'page',
            'status',
        ]