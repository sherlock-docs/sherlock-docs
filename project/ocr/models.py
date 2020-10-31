import os

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.core.files import File

from .tasks import (recognize_document_via_ocr, recognize_document_via_tesseract, recognize_docx_document,
                    recognize_doc_document, split_pdf_into_pages, pdf_to_jpg)
from .utils import is_pdf, is_docx, is_doc, is_image


class DocumentType(models.Model):
    name = models.CharField(max_length=256, verbose_name='Тип документа')
    attributes = JSONField(verbose_name='Атрибуты', null=True, blank=True)

    class Meta:
        verbose_name = 'Тип документа'
        verbose_name_plural = 'Типы документов'
        ordering = ['-id']

    def __str__(self):
        return f"{self.name}"


class Document(models.Model):
    file = models.FileField(upload_to='docs', verbose_name='Оригинальный файл документа')
    file_type = models.CharField(max_length=255, blank=True, null=True, verbose_name='Временный тип файлов')
    type = models.ForeignKey(DocumentType, on_delete=models.CASCADE, null=True, verbose_name='Тип документа')
    # Статус
    QUEUE = 'Q'
    PROCESS = 'P'
    COMPLETED = 'C'
    STATUS_CHOICES = [
        (QUEUE, 'В очереди'),
        (PROCESS, 'В процессе'),
        (COMPLETED, 'Распознан')
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=QUEUE, verbose_name='Статус распознавания')
    ocr_text = models.TextField(null=True, blank=True,
                                verbose_name='Распознанный текст из документа(без сегментации) через OCR')
    tesseract_text = models.TextField(null=True, blank=True,
                                      verbose_name='Распознанный текст из документа(без сегментации) через Tesseract')
    doc_text = models.TextField(null=True, blank=True,
                                verbose_name='Распознанный текст из документа(без сегментации) через Antiword или ')

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
        ordering = ['-id']

    @property
    def type_name(self):
        return self.type.name

    def save(self, *args, **kwargs):
        super(Document, self).save(*args, **kwargs)
        if self.status == self.QUEUE:
            self.status = self.PROCESS
            self.save()
            if is_pdf(self.file.path):
                # recognize_document_via_ocr.delay(self.id, page=True)
                # Разбиваем PDF по страницам.
                split_pdf_into_pages.delay(self.pk)
            elif is_doc(self.file.path):
                # FIXME: Разбивака по старницам + продумать, как структурировать тектс.
                recognize_doc_document.delay(self.id)
            elif is_docx(self.file.path):
                # FIXME: Разбивака по старницам + продумать, как структурировать тектс.
                recognize_docx_document.delay(self.id)
            elif is_image(self.file.path):
                page, created = PageDocument.objects.get_or_create(parent_document_id=self.pk, page=1)
                # Прикладываем файл.
                with open(self.file.path, 'rb') as f:
                    filename = os.path.splitext(os.path.basename(self.file.path))[0]
                    page.jpg_file.save(filename + '.jpg', File(f), save=True)


class PageDocument(models.Model):
    parent_document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='pages', verbose_name='Основной документ')
    page = models.PositiveIntegerField(default=1, verbose_name='Номер страницы')
    file = models.FileField(upload_to='docs/pages', verbose_name='Постраничный файл документа')
    jpg_file = models.FileField(upload_to='docs/pages/jpg', verbose_name='Постраничный файл документа')
    type = models.ForeignKey(DocumentType, on_delete=models.CASCADE, null=True, verbose_name='Тип документа')
    # Статус
    QUEUE = 'Q'
    PROCESS = 'P'
    COMPLETED = 'C'
    STATUS_CHOICES = [
        (QUEUE, 'В очереди'),
        (PROCESS, 'В процессе'),
        (COMPLETED, 'Распознан')
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=QUEUE, verbose_name='Статус распознавания')
    ocr_text = models.TextField(null=True, blank=True,
                                verbose_name='Распознанный текст из документа(без сегментации) через OCR')
    tesseract_text = models.TextField(null=True, blank=True,
                                      verbose_name='Распознанный текст из документа(без сегментации) через Tesseract')
    doc_text = models.TextField(null=True, blank=True,
                                verbose_name='Распознанный текст из документа(без сегментации) через Antiword или ')

    class Meta:
        verbose_name = 'Страница из документа'
        verbose_name_plural = 'Страницы из документов'
        ordering = ['-id']

    @property
    def type_name(self):
        return self.type.name

    def save(self, *args, **kwargs):
        super(PageDocument, self).save(*args, **kwargs)
        if self.file:
            if is_image(self.file.path):
                if not self.tesseract_text:
                    recognize_document_via_tesseract.delay(self.id, page=True)
                if not self.ocr_text:
                    recognize_document_via_ocr.delay(self.id, page=True)
            elif is_pdf(self.file.path):
                pdf_to_jpg.delay(self.id)
        elif self.jpg_file:
            if is_image(self.jpg_file.path):
                if not self.tesseract_text:
                    recognize_document_via_tesseract.delay(self.id, page=True, jpg_file=True)
                if not self.ocr_text:
                    recognize_document_via_ocr.delay(self.id, page=True, jpg_file=True)


class FormalizedDocument(models.Model):
    type = models.ForeignKey(
        DocumentType,
        verbose_name='Тип документа',
        on_delete=models.PROTECT,
        related_name='formalized_docs'
    )
    parent = models.ForeignKey(
        PageDocument,
        verbose_name='Родитель',
        on_delete=models.PROTECT,
        related_name='formalized_docs'
    )
    text = models.TextField(
        verbose_name='Распознанный текст',
        blank=True,
        null=True
    )
    data = JSONField(
        verbose_name='Атрибуты документа',
        blank=True,
        null=True
    )

    def __str__(self):
        return f'Документ "{self.type}"'

    class Meta:
        verbose_name = 'Формализованный документ'
        verbose_name_plural = 'Формализованные документы'
