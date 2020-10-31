import os
import requests
import logging
import pytesseract
import subprocess

from celery import shared_task
from docx import Document as DocxDocument
from PyPDF2 import PdfFileWriter, PdfFileReader
from PIL import Image

from django.core.files import File
from django.conf import settings

from wand.image import Image

@shared_task
def recognize_document_via_ocr(pk, page=False, jpg_file=True):
    """
    Распознавание документа посредсрвтом OCR
    """
    from .models import Document, PageDocument
    doc = PageDocument.objects.get(pk=pk) if page else Document.objects.get(pk=pk)
    path_to_doc = doc.jpg_file.path if jpg_file else doc.file.path
    try:
        # Получаем текст из документа.
        full_text = ''
        file_name = doc.file.path.split('/')[-1]
        with open(path_to_doc, 'rb') as f:
            url = f"{settings.OCR_URL}{file_name}"
            res = requests.post(url, data=f)
            res.encoding = 'utf-8'
            if res.ok:
                pages = res.json().get('result', {}).get('pages', [])
                for page in pages:
                    full_text += page.get('text', '')
            elif res.status_code == 503:
                pages = res.json().get('result', {}).get('pages', [])
                for page in pages:
                    full_text += page.get('text', '')

        # Сохраняем данные в базу.
        doc.ocr_text = full_text
        doc.status = doc.COMPLETED
        doc.save()
        return True
    except Exception as err:
        logging.warning(err)
        doc.status = doc.QUEUE
        doc.save()

    return False


@shared_task
def recognize_document_via_tesseract(pk, page=False, jpg_file=False):
    """
    Распознавание документа посредсрвтом Tesseract
    """
    from .models import Document, PageDocument
    doc = PageDocument.objects.get(pk=pk) if page else Document.objects.get(pk=pk)
    path_to_doc = doc.jpg_file.path if jpg_file else doc.file.path
    try:
        # Получаем текст из документа.
        custom_config = r'--oem 3 --psm 6'
        full_text = pytesseract.image_to_string(
            path_to_doc,
            lang='rus',
            config=custom_config
        )
        # Сохраняем данные в базу.
        doc.tesseract_text = full_text
        doc.status = doc.COMPLETED
        doc.save()
        return True
    except Exception as err:
        logging.warning(err)
        doc.status = doc.QUEUE
        doc.save()

    return False


@shared_task
def recognize_doc_document(pk, page=False):
    """Метод возвращает текст из файла DOC"""
    from .models import Document, PageDocument
    doc = PageDocument.objects.get(pk=pk) if page else Document.objects.get(pk=pk)
    try:
        p = subprocess.Popen(['antiword', doc.file.path], stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
        # Сохраняем данные в базу.
        doc.doc_text = stdout.decode('ascii', 'ignore').lower()
        doc.status = doc.COMPLETED
        doc.save()
        return True
    except Exception as err:
        logging.warning(err)
        doc.status = doc.QUEUE
        doc.save()

    return False


@shared_task
def recognize_docx_document(pk, page=False):
    """Метод возвращает текст из файла DOCX"""
    from .models import Document, PageDocument
    doc = PageDocument.objects.get(pk=pk) if page else Document.objects.get(pk=pk)
    try:
        document = DocxDocument(doc.file.path)
        text = []
        for para in document.paragraphs:
            if para.text.strip():
                text.append(para.text)
        # Сохраняем данные в базу.
        doc.doc_text = '\n\n'.join(text).lower()
        doc.status = doc.COMPLETED
        doc.save()
        return True
    except Exception as err:
        logging.warning(err)
        doc.status = doc.QUEUE
        doc.save()

    return False


@shared_task
def split_pdf_into_pages(pk):
    """
    Метод конвертирует каждую страницу PDF-файла в отдельный PDF-файл
    и сохраняет их по переданному пути.
    :param file_path: (str) Путь к файлу.
    :return: None.
    """
    from .models import Document, PageDocument
    doc = Document.objects.get(pk=pk)
    try:
        path_dir_name = os.path.dirname(doc.file.path)
        filename = os.path.splitext(os.path.basename(doc.file.path))[0]
        with open(doc.file.path, "rb") as f:
            input_pdf = PdfFileReader(f)
            for i in range(input_pdf.numPages):
                i += 1
                page_pdf = PdfFileWriter()
                page_pdf.addPage(input_pdf.getPage(i))
                path_to_file = f'{path_dir_name}/{filename}_page_{i}.pdf'
                with open(path_to_file, "wb") as outputStream:
                    page_pdf.write(outputStream)
                    page, created = PageDocument.objects.get_or_create(parent_document_id=pk, page=i)
                    # Прикладываем файл.
                    with open(path_to_file, 'rb') as f:
                        page.file.save(f'{filename}_page_{i}.pdf', File(f), save=True)
        return True
    except Exception as err:
        logging.warning(err)
        doc.status = doc.QUEUE
        doc.save()

    return False


@shared_task
def split_pdf_into_img_pages(pk):
    """
    Метод конвертирует каждую страницу PDF-файла в отдельный PNG-файл
    и сохраняет их по переданному пути.
    :param file_path: (str) Путь к файлу.
    :return: None.
    """
    from .models import Document, PageDocument
    import fitz

    doc = Document.objects.get(pk=pk)
    path_dir_name = os.path.dirname(doc.file.path)
    filename = os.path.splitext(os.path.basename(doc.file.path))[0]
    try:
        pdf = fitz.open(doc.file.path)
        for i in range(len(pdf)):
            i += 1
            path_to_png_file = f'{path_dir_name}/{filename}_page_{i}.png'
            path_to_jpg_file = f'{path_dir_name}/{filename}_page_{i}.jpg'
            for img in pdf.getPageImageList(i):
                xref = img[0]
                pix = fitz.Pixmap(pdf, xref)
                if pix.n < 5:  # this is GRAY or RGB
                    pix.writePNG(path_to_png_file)
                    im = Image.open(path_to_png_file)
                    rgb_im = im.convert('RGB')
                    rgb_im.save(path_to_jpg_file)
                else:  # CMYK: convert to RGB first
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix1.writePNG(path_to_png_file)
                    im = Image.open(path_to_png_file)
                    rgb_im = im.convert('RGB')
                    rgb_im.save(path_to_jpg_file)
                    pix1 = None

                page, created = PageDocument.objects.get_or_create(parent_document_id=pk, page=i)
                # Прикладываем файл.
                with open(path_to_jpg_file, 'rb') as f:
                    page.jpg_file.save(filename + 'jpg', File(f), save=True)
                pix = None

        return True
    except Exception as err:
        logging.warning(err)
        doc.status = doc.QUEUE
        doc.save()

    return False


@shared_task
def pdf_to_jpg(pk):
    """
    Метод конвертирует каждую страницу PDF-файла в отдельный PNG-файл
    и сохраняет их по переданному пути.
    :param file_path: (str) Путь к файлу.
    :return: None.
    """
    from .models import PageDocument
    import fitz

    doc = PageDocument.objects.get(pk=pk)
    path_dir_name = os.path.dirname(doc.file.path)
    origin_filename = os.path.splitext(os.path.basename(doc.file.path))[0]
    try:
        pdf = fitz.open(doc.file.path)
        for i in range(len(pdf)):
            i += 1
            filename = f'{origin_filename}_page_{i}'
            path_to_png_file = f'{path_dir_name}/{filename}.png'
            path_to_jpg_file = f'{path_dir_name}/{filename}.jpg'
            for img in pdf.getPageImageList(i):
                xref = img[0]
                pix = fitz.Pixmap(pdf, xref)
                if pix.n < 5:  # this is GRAY or RGB
                    pix.writePNG(path_to_png_file)
                    im = Image.open(path_to_png_file)
                    rgb_im = im.convert('RGB')
                    rgb_im.save(path_to_jpg_file)
                else:  # CMYK: convert to RGB first
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix1.writePNG(path_to_png_file)
                    im = Image.open(path_to_png_file)
                    rgb_im = im.convert('RGB')
                    rgb_im.save(path_to_jpg_file)
                    pix1 = None
                # Прикладываем файл.
                with open(path_to_jpg_file, 'rb') as f:
                    doc.jpg_file.save(filename + '.jpg', File(f), save=True)
                pix = None

        return True
    except Exception as err:
        logging.warning(err)
        doc.status = doc.QUEUE
        doc.save()

    return False


@shared_task
def make_jpg_from_pdf(file_path):
    jpg_paths = []
    with Image(filename=file_path, resolution=settings.OPTIMAL_RESOLUTION) as pdf:
        jpg = pdf.convert('jpeg')
        i = 1
        try:
            for img in jpg.sequence:
                with Image(image=img) as page:
                    path_dir_name = os.path.dirname(file_path)
                    filename = '{}/{}.jpg'.format(path_dir_name, i)
                    page.save(filename=filename)
                    i += 1
                    jpg_paths.append(filename)
        finally:
            jpg.destroy()
        return sorted(jpg_paths)