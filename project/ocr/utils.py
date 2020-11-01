import os
import re
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


def classifier(text):
    # Типы документов
    city_planners_type = 'Свидетельство об утверждении архитектурно-градостроительного решения'
    bti_type = 'Технический паспорт (МосгорБТИ, МособлБТИ,  Ростехинвентаризация, ВИСХАГИ)'
    excerpt_type = 'Выписка из ЕГРН'
    explic_type = 'Экспликация к архивному поэтажному плану'
    lease_contract_type = 'Договор аренды земельного участка'
    building_permit_type = 'Разрешение на строительство'
    commissioning_type = 'Разрешение на ввод объекта в эксплуатацию'
    other_type = 'Прочие типы документов'
    # 'Технический паспорт на здание'
    # 'Технический паспорт на домовладение (земельный участок)'
    # 'Кадастровый паспорт'
    # 'Плановое (реставрационное) задание'
    # 'Разрешение на производство подготовительных и основных строительно-монтажных работ'
    # 'Заключение Могосэкспертизы'
    # 'Договор'
    # 'Градостроительное заключение'
    # 'Акт государственной приемочной комиссии о приемке в эксплуатацию законченного строительством объекта'
    # 'Распоряжение префекта'
    # 'Выписка из реестра Федерального имущества'
    # 'Свидетельство о регистрации права'
    # 'Распоряжение'
    # 'Определение'
    # 'Акт'
    # 'Разрешение'
    # 'Заключение'
    # 'Проект'
    # 'Письмо'
    # 'Пояснительная записка'
    # 'Поэтажный план'
    # 'Выписка из ЕГРН'
    # 'Акт приемки в эксплуатацию законченного строительства'
    # 'Выписка из постановления'
    # 'Инвентаризационная карточка'
    # 'Извлечение из технического паспорта'
    # 'Разрешение на производство строительно-монтажных работ'
    # 'Выписка из реестра Федерального имущества'
    # 'Свидетельство о регистрации права'
    # 'Распоряжение'
    # 'Определение'
    # 'Акт'
    # 'Разрешение'
    # 'Заключение'
    # 'Проект'
    # 'Письмо'
    # 'Пояснительная записка'
    # 'Поэтажный план'
    # 'Акт приемки в эксплуатацию законченного строительства'
    # 'Выписка из постановления'
    # 'Инвентаризационная карточка'
    # 'Извлечение из технического паспорта'
    # 'Разрешение на производство строительно-монтажных работ'
    # Сущности для классификации
    building_permit_001 = 'pазрешение на строительство'
    building_permit_002 = 'статьей 51 градостроительного'

    commissioning_001 = 'разрешение на ввод объекта'
    commissioning_002 = 'руководствуясь статьей 55 градостроительного'
    commissioning_003 = 'продолжение разрешения на ввод'

    bti_001 = 'технический паспорт'
    bti_002 = 'технического паспорта'
    bti_003 = 'нежилые'

    explic_001 = 'экспликация'

    excerpt_001 = 'выписка из технического'

    lease_contract_001 = 'договор аренды'
    lease_contract_002 = 'аренды земли'
    lease_contract_003 = 'о предоставлении участка'
    lease_contract_004 = 'арендодатель'
    lease_contract_005 = 'на условиях аренды'
    lease_contract_006 = 'по оформлению права пользования'

    city_planners_001 = 'свидельство об утверждении'
    city_planners_002 = 'рассмотрение на рабочей комиссии'
    city_planners_003 = 'выписка из протокола'
    city_planners_004 = 'авторы проекта'

    samples = [excerpt_001,
               explic_001,
               building_permit_001, building_permit_002,
               commissioning_001, commissioning_002, commissioning_003,
               bti_001, bti_003,
               lease_contract_001, lease_contract_002, lease_contract_003, lease_contract_004,
               lease_contract_005, lease_contract_006,
               city_planners_001, city_planners_002, city_planners_003, city_planners_004]

    answers = [excerpt_type,
               explic_type,
               building_permit_type, building_permit_type,
               commissioning_type, commissioning_type, commissioning_type,
               bti_type, bti_type,
               lease_contract_type, lease_contract_type, lease_contract_type, lease_contract_type, lease_contract_type,
               city_planners_type, city_planners_type, city_planners_type, city_planners_type]

    text = text.lower()
    text = re.sub(r'\s+', ' ', text, flags=re.I)
    text = re.sub(r'\n', ' ', text)

    k = 0
    for i in range(len(samples)):
        result = re.findall(samples[i], text)

        if result:
            return answers[i]
            k += 1
            break
        if k == 18:
            return other_type
        else:
            k += 1

    return other_type