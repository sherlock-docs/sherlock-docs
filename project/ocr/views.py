import django_filters
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from ocr.pagination import ResultsSetPagination
from ocr.models import Document, DocumentType
from ocr.serializers import DocumentSerializer, DocumentTypeSerializer
from ocr.filters import DocumentFilter


class DocumentView(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    filter_class = DocumentFilter
    pagination_class = ResultsSetPagination
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
    )


class DocumentTypeView(mixins.ListModelMixin, GenericViewSet):
    """
    Document Types.
    """
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer