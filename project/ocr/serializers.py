from rest_framework import serializers
from drf_extra_fields.fields import Base64FileField
from ocr.models import Document, DocumentType, PageDocument


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = "__all__"


class PageDocumentSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(source='type.name')
    status = serializers.ReadOnlyField(source='get_status_display')

    class Meta:
        model = PageDocument
        fields = [
            "page",
            "status",
            "type",
            "file",
            "text",
            "doc_text",
            "data",
        ]
        read_only_fields = ["text", "doc_text", "data"]


class DocumentSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField(source='get_status_display')
    pages = PageDocumentSerializer(many=True, read_only=True)
    file = Base64FileField(required=True)

    class Meta:
        model = Document
        fields = "__all__"
        read_only_fields = ["text", "doc_text", "pages"]
