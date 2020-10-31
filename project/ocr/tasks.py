import os
import requests
import logging
import pytesseract
import subprocess

from wand.image import Image as WandImage
from celery import shared_task
from docx import Document as DocxDocument
from PyPDF2 import PdfFileWriter, PdfFileReader
from PIL import Image

from django.core.files import File
from django.conf import settings

from .utils import classifier


@shared_task
def recognize_document_via_tesseract(pk, page=False):
    """
    Распознавание документа посредсрвтом Tesseract
    """
    from .models import Document, PageDocument, DocumentType
    doc = PageDocument.objects.get(pk=pk) if page else Document.objects.get(pk=pk)
    try:
        # Получаем текст из документа.
        custom_config = r'--oem 3 --psm 6'
        full_text = pytesseract.image_to_string(
            doc.file.path,
            lang='rus',
            config=custom_config
        )
        # Сохраняем данные в базу.
        doc.text = full_text
        # Классифицируем
        if full_text:
            doc_type = classifier(full_text)
            doc_type, created = DocumentType.objects.get_or_create(name=doc_type)
            doc.type = doc_type
        doc.status = doc.COMPLETED
        doc.save()
        return True
    except Exception as err:
        logging.warning(err)
        doc.status = doc.FAILED
        doc.save()

    return True


@shared_task
def recognize_doc_document(pk, page=False):
    """Метод возвращает текст из файла DOC"""
    from .models import Document, PageDocument, DocumentType
    doc = PageDocument.objects.get(pk=pk) if page else Document.objects.get(pk=pk)
    try:
        p = subprocess.Popen(['antiword', doc.file.path], stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
        # Сохраняем данные в базу.
        doc.doc_text = stdout.decode('ascii', 'ignore').lower()
        if doc.doc_text:
            # Классифицируем
            if doc.doc_text:
                doc_type = classifier(doc.doc_text)
                doc_type, created = DocumentType.objects.get_or_create(name=doc_type)
                doc.type = doc_type
        doc.status = doc.COMPLETED
        doc.save()
        return True
    except Exception as err:
        logging.warning(err)
        doc.status = doc.FAILED
        doc.save()

    return True


@shared_task
def recognize_docx_document(pk, page=False):
    """Метод возвращает текст из файла DOCX"""
    from .models import Document, PageDocument, DocumentType
    doc = PageDocument.objects.get(pk=pk) if page else Document.objects.get(pk=pk)
    try:
        document = DocxDocument(doc.file.path)
        text = []
        for para in document.paragraphs:
            if para.text.strip():
                text.append(para.text)
        # Сохраняем данные в базу.
        doc.doc_text = '\n\n'.join(text).lower()
        if doc.doc_text:
            # Классифицируем
            if doc.doc_text:
                doc_type = classifier(doc.doc_text)
                doc_type, created = DocumentType.objects.get_or_create(name=doc_type)
                doc.type = doc_type
        doc.status = doc.COMPLETED
        doc.save()
        return True
    except Exception as err:
        logging.warning(err)
        doc.status = doc.FAILED
        doc.save()

    return True


@shared_task
def split_pdf_to_img_pages(pk):
    """
    Метод конвертирует каждую страницу PDF-файла в отдельный JPG-файл
    и сохраняет их по переданному пути.
    :param file_path: (str) Путь к файлу.
    :return: None.
    """
    from .models import Document, PageDocument
    doc = Document.objects.get(pk=pk)
    try:
        path_dir_name = os.path.dirname(doc.file.path)
        origin_filename = os.path.splitext(os.path.basename(doc.file.path))[0]
        with WandImage(filename=doc.file.path, resolution=settings.OPTIMAL_RESOLUTION) as pdf:
            jpg = pdf.convert('jpeg')
            i = 1
            try:
                for img in jpg.sequence:
                    with WandImage(image=img) as page_pdf:
                        filename = f'{origin_filename}-{i}'
                        path_to_filename = f'{path_dir_name}/{filename}.jpg'
                        page_pdf.save(filename=path_to_filename)
                        page, created = PageDocument.objects.get_or_create(parent_document_id=pk, page=i)
                        # Прикладываем файл.
                        with open(path_to_filename, 'rb') as f:
                            page.file.save(filename + '.jpg', File(f), save=True)
                        i += 1
            finally:
                jpg.destroy()
        return True
    except Exception as err:
        logging.warning(err)
        doc.status = doc.FAILED
        doc.save()
    return True
