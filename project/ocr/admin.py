from django.contrib import admin
from .models import (Document, DocumentType, PageDocument)


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'status')
    list_filter = ('status', )


@admin.register(PageDocument)
class PageDocumentAdmin(admin.ModelAdmin):
    search_fields = ('text', )
    list_display = ('id', 'parent_document', 'page', 'file', 'type', 'status')
    list_filter = ('type', 'status', 'page')
