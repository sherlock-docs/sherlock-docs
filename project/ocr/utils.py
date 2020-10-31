import os
import magic
import PIL.Image as PilImage
from django.conf import settings


def is_image(file_path):
    try:
        name, extension = file_path.split('.')
    except ValueError:
        name, extension = file_path, ''
    if extension in settings.EXTENSIONS_TO_CROP:
        return True

    return False

def is_pdf(file_path):
    """
    Метод проверяет тип переданного файла,
    если тип PDF - возвращает True,
    иначе - возвращает False.
    :param file_path: (str) Путь к файлу.
    :return: Boolean.
    """
    if magic.from_file(file_path, mime=True) == 'application/pdf':
        return True
    return False

def is_doc(file_path):
    """
    Метод проверяет тип переданного файла,
    если тип DOC - возвращает True,
    иначе - возвращает False.
    :param file_path: (str) Путь к файлу.
    :return: Boolean.
    """
    if magic.from_file(file_path, mime=True) == 'application/msword':
        return True
    return False

def is_docx(file_path):
    """
    Метод проверяет тип переданного файла,
    если тип DOCX - возвращает True,
    иначе - возвращает False.
    :param file_path: (str) Путь к файлу.
    :return: Boolean.
    """
    if magic.from_file(file_path,
                       mime=True) == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        return True
    return False

def is_file_too_long(file_path):
    """
    Метод проверяетя вертикальную длину изображения
    и если длина превышает ширину изображения в 2 раза,
    возвращает True, иначе False.
    :param file_path: Путь к файлу с изображением.
    :return: Boolean.
    """
    if is_image(file_path):
        with PilImage.open(file_path) as file:
            width = file.size[0]
            height = file.size[1]
            if height > width * 2:
                return True
    return False