import os
import cv2
import numpy as np
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


# Список атрибутов
BONES_FRONT = {
    0: 'общая площадь',
    1: 'наземная площадь',
    2: "поднемная площадь",
    3: "верхняя отметка",
    4: 'площадь застройки',
    5: 'объем',
    6: "этажность",
    7: "проектная организация",
    8: "авторы проекта",
    9: "руководитель авторов",
    10: "разрешение на проектирование",
    11: "застройшик",
    12: "заказчик",
    13: "функциональное назначение",
    14: "наименование объекта",
    15: "владение",
    16: "корпус",
    17: "строение",
    18: "адрес",
    19: "район",
    20: "округ",
    21: "город",
    24: "регистрационный номер",
    25: "код строительного объекта",
    26: "код недвижимости",
    27: "дата"
}


### Парс первой страницы ###

def parse_front(img_front):
    ### cv предобработка
    gray = cv2.cvtColor(img_front, cv2.COLOR_BGR2GRAY)
    thresh_inv = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    blur = cv2.GaussianBlur(thresh_inv, (1, 1), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    ### находим контуры
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    ### переменные для присвоения номеров
    UPD = [54, 55, 60, 122, 129, 135, 136, 233, 250, 289, 450, 464, 475,
           508, 529, 558, 559, 560, 567, 576, 599, 620, 734, 771, 842]
    KEYS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 24, 25, 26]

    for key_, num in zip(UPD, KEYS):
        x, y, w, h = cv2.boundingRect(contours[key_])

        ### Мужики, тут можно изменить путь сохранения
        plt.imsave('{}'.format(num) + '.png', img_front[y:h + y, x:w + x])


### Парс второй страницы ###

def parse_back(img_back):
    gray = cv2.cvtColor(train_02, cv2.COLOR_BGR2GRAY)
    thresh_inv = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    blur = cv2.GaussianBlur(thresh_inv, (1, 1), 0)

    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    x, y, w, h = cv2.boundingRect(contours[715])

    ### Путь сохранения можно менять
    plt.imsave('{}'.format(27) + '.png', train_02[y:h + y, x:w + x])
