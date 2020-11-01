import logging

from rest_framework import serializers
from drf_extra_fields.fields import Base64FileField

from .models import Document, DocumentType, PageDocument


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


class DocumentBase64FileField(Base64FileField):
    ALLOWED_TYPES = ['pdf', 'png', 'jpg', 'jpeg', 'tiff']

    def get_file_extension(self, filename, decoded_file):
        import imghdr
        from PyPDF2 import PdfFileReader
        from PyPDF2.utils import PdfReadError
        import io

        try:
            PdfFileReader(io.BytesIO(decoded_file))
            return 'pdf'
        except PdfReadError as e:
            logging.warning(e)

        try:
            extension = imghdr.what(filename, decoded_file)
            return 'jpg' if extension == 'jpeg' else extension
        except FileExistsError as e:
            logging.warning(e)
        try:
            extension = imghdr.what(filename, decoded_file)
            return 'tiff' if extension == 'tiff' else extension
        except FileExistsError as e:
            logging.warning(e)


class DocumentSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField(source='get_status_display')
    pages = PageDocumentSerializer(many=True, read_only=True)
    file = DocumentBase64FileField(required=True)

    class Meta:
        model = Document
        fields = "__all__"
        read_only_fields = ["text", "doc_text", "pages"]
