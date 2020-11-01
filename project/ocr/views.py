import django_filters
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .pagination import ResultsSetPagination
from .models import Document, DocumentType, PageDocument
from .serializers import DocumentSerializer, DocumentTypeSerializer, PageDocumentSerializer
from .filters import DocumentFilter, PageDocumentFilter


class DocumentView(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    filter_class = DocumentFilter
    pagination_class = ResultsSetPagination
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
    )


class PageDocumentView(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = PageDocument.objects.all().order_by('-page')
    serializer_class = PageDocumentSerializer
    filter_class = PageDocumentFilter
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