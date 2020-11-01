from django.contrib import admin
from .models import (Document, DocumentType, PageDocument)
import re

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
    list_display = ('id', 'parent_document', 'page', 'file', 'type', 'status', 'search_result')
    list_filter = ('type', 'status', 'page')

    def changelist_view(self, request, extra_context=None):
        self.q = request.GET.get('q')
        return super(PageDocumentAdmin, self).changelist_view(request, extra_context=extra_context)

    def search_result(self, obj):
        """Метод который добавялем столбец в котором выводиться кусок текста
        с вхождением строки поиска + n кол-во символов"""
        n = 30 # Количество символов
        result = ""
        if self.q:
            p = re.compile(self.q, re.IGNORECASE)
            for m in p.finditer(obj.text):
                start, end = m.span()
                result += "[{}], ".format(obj.text[start:end + n])
        return result
