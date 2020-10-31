from django.contrib import admin
from ocr.models import (Document, DocumentType)


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'type', 'status')
    list_filter = ('type', 'status')