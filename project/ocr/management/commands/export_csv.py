import re
import time
import hashlib
from django.db import connections
from django.core.cache import cache
from collections import OrderedDict
from django.core.management import BaseCommand
from django.db import connections
from django.conf import settings
import os
import glob
import pathlib
from ocr.models import Document, PageDocument
import pandas as pd

from ocr.tasks import (recognize_document_via_tesseract, recognize_docx_document,
                    recognize_doc_document)
from PyPDF2 import PdfFileWriter, PdfFileReader
from PIL import Image

class Command(BaseCommand):
    def handle(self, *args, **options):
        d = {
            'Технический паспорт(Экспликация)': [
                """ГБУ Московское городское бюро технической инвентаризации
ГБУ МосгорБТИ
Адрес: 125009, г. Москва, Малый Гнездниковский пер., д. 1, стр. 7
Телефон: 8 (495) 629-02-80
ЭКСПЛИКАЦИЯ
Стр. 1
Адрес (иное описание местоположения): я):
город Москва, улица Шеногина, дом 3, строение 2
Помещение № Тип: Нежилое
Сведениями о соблюдении требований пункта 4 части 17 статьи 51 Градостроительного кодекса Российской Федерации ГБУ МосгорБТИ не располагает (ком. 12,13)
Площадь помещений
Этаж №№ комнат
Характеристики
комнат и помещений
Площадь общая, кв.м.
Всего
в том числе
вспомогательного
использования (с коэф.), кв. м Вы- сота,
в том числе
основн. вспом. лоджий балконов прочих
см.
Примечание
Дата
обследования
подвал 1
кладовая
лестница
14,2
3,3
14,2
229 учрежд. 28.09.2010 г. учрежд.
229 28.09.2010 г.
коридор
3,3
3,3
229 2010 г.
коридор
коридор
2,9
9,9
2,9
9,9
229 учрежд.
229
28.09.2010 г. учрежд. 28.09.2010 г.
6
8
9
10
комната отдыха
прочее
служебное
служебное
служебное
20,7
4,6
12,2
8,3
4,6
12,2
8,3
20,7
229 учрежд.
28.09.2010 г. прочая 229 про 28.09.2010 г. 229 учр учрежд. 28.09.2010 г. 229 учрежд. 28.09.2010 г. учрежд.
229 28.09.2010 г.
11
коридор
3,6
3,6
учрежд.
229 28.09.2010 г.
12
кладовая
8,6
8,6
учрежд.
229 28.09.2010 г.
13
мастерская
8,2
8,2
г.
14
душевая
7,8
7,8
229 учрежд.
28.09.2010 г.
15
коридор
11,8
11,8
229 Учрежд.
28.09.2010 г.
16
17
душевая
электрощитовая
8,4
6,0
6,0
8,4
229 учрежд.
28.09.2010 г. прочая
229 28.09.2010 г.
18
19
коридор
бойлерная
8,2
8,22
5,3
229 учрежд.
266
28.09.2010 г. прочая 28.09.2010 г.""",
                """Восточное-2 ТБТИ
экспликация
По адресу: Щербаковская ул., 52, корп
лист
Помещение N I Тип: Прочие
ф.25
Последнее обследование 6.11.2001
Этаж комн.
NN Характеристики
комнат и помещений
Площади Вы- без - в т.ч. летни х со- летних основ. вспом. лодж. балк. проч. та
п
тамбур тамбур пом. подсобное венткамера венткамера венткамера умывальная 8 уборная 9 уборная 10 уборная 11 ударная 12 умывальная 13 аппаратная 14 аппаратная 15 аппаратная 16 шлюз 17 тамбур 18 коридор 19 отдел. машинное 20 насосная 21 насосная 22 пом. техническое 23 электращитовая 24 электрощитовая 25 электрощитовая 26 электрощитовая 27 электрощитовая 28 электрощитовая 29 коридор 30 электрощитовая 31 электращитовая 32 венткамера 33 коридор 34 венткамера 35 венткамера 36 венткамера 37 пом. подсобное 38 пом. подсобное 39 пом. подсобное 40 пом. подсобное 41 пом. техническое 42 пом. техническое
5,4 11,0 22,9 10,8 10,8 1,8 1,7
1,8 1,7 11,8 13,3 11,0 12,7 10,4 11,9 11,4 11,4 13,1 13,1 13,1 13,1 17,0 17,0 5,6 9,8 13,1 13,1 43,0 43,0 30,2 30,2 653,4 653,4 3,2 3,2 12,1 12,1 52,6 52,6 4,0 4,0 2,6 2,6 2,8 2,8 2,8 2,4 2,4 2,3 2,3 3,5 3,5 2,0 7,0 7,0 2,0 2,0 39,3 39,3 1,8 5,6 3,4 5,3 5,8 5,8 4, 4,5
5,4 прочая 11,0 прочая 22,9 прочая прочая прочая прочая 11,8 учрежд. 13,3 учрежд. 11,0 учрежд. 12,7 учрежд. 10,4 учрежд. 11,9 учрежд. прочая прочая прочая прочая 5,6 прочая 9,8 прочая прочая прочая прочая прочая прочая прочая прочая прочая прочая прочая 2,8 прочая прочая прочая прочая 2,0 прочая прочая прочая прочая 1,8 прочая 5,6 прочая 3,4 прочая 5,3 прочая прочая прочая
510""",
                """Северо-Восточное ТБТИ
Э К С П Л И К А Ц И Я
По адресу: Ярославское шоссе, 40
стр.
Помещение N I Тип: Прочие
ф.25
Последнее обследование 4.04.2006
Этаж NN Характеристики
комн.
комнат и помещений
Общая площадь
Площадь помещений Вы- вспомогат. использ. со-
(с коэф.)
та
в т.ч.
в т.ч.
всего основ. вспом. лодж. балк. проч
п
5 6
8 9 10 11 12 13 14 15 16 17 18 19 20
тамбур 10,2 бойлерная 69,7 пом. техническое 2,9 гараж 212,5 212,5 склад 301,4 301,4 пом. подсобное 2,2 пом. техническое 21,9 лестница 18,3 венткамера 38,9 коридор 13,4 подъемник 1,2 раздевалка 10, 8 зал спортивный 40,8 40,8 пом. подсобное 7,5 уборная 2,2 душевая 2,1 сауна 10,2 10,2 бассейн 34,3 34,3 комн. для отдыха 47,0 47,0 тамбур 1,1
10,2 прочая 69,7 прочая 2,9 прочая гараж. складс. 2,2 прочая 21,9 прочая 18,3 прочая 38,9 прочая 13,4 прочая 1,2 прочая 10,8 культур культур 7,5 культур 2,2 культур 2,1 культур культур культур культур 1,1 культур
550
Итого
по помещению 848,6 646,2 202,4 -Нежилые помещения всего 848,6 646,2 202,4 в т.ч. Складские
Гаражи Культпросветит. Прочие
301,4 301,4 212,5 212,5 156,0 132,3 178,7
23,7 178,7
Итого
по этажу п
848,6 646,2
202,4 202,4
в т.ч. Складские
Гаражи Культпросветит. Прочие
301,4 301,4 212,5 212,5 156,0 132,3 178,7
23,7 178,7""",
            ],
            'Технический паспорт': [
                """ТЕХНИЧЕСКИЙ ПАСПОРТ
        Кварт. №
        2401
        Склад
        на
        Инвент. №
        8
        (назначение здания)
        (вместимость)
        Шифр фонда гос
        по
        ул. Шеногина
        дом № 3 3
        стр. корп.№
        Шифр проекта
        Север-Западный
        АО г. Москвы
        1. Общие сведения
        Владелец
        ОАО "Домострой"
        Число этажей
        Год постройки
        1954 переоб-вано пристроено
        Год последнего кап. Рем-та
        Кроме того, имеется:
        подвал
        цокольный этаж,
        мансарда,
        мезонин
        (подчеркнуть)
        Материал крыши рубероид Фасад Без отделки Число лестниц Уборочная площадь общих коридоров и мест общ. пользов Объем
        599 куб. м
        шт. их уборочная площадь
        площадь крыши площадь фасадов
        кв.м.
        кв.м.
        205
        кв.м.
        кв.м.
        Общая площадь по зданию
        153,8
        кв.м., в т.ч. общей, без учета балконов и лоджий
        кв.м.
        из них
        a. Жилые помещения: Общ. площ.
        кв.м., в т.ч. общей пл-ди, без уч. балконов и лоджий
        жилой площади
        кв. м.
        Общая площадь, относящаяся к общему имуществу многоквартир дома
        кв.м.
        A. Распределение жилой площади
        количество
        Текущие изменения
        количество
        коли количество
        Жилая площадь находится
        6
        14
        В квартирах
        В помещен коридоре, системы В общежитиях
        4
        Служебная жилая площадь Маневренная жилая площадь
        Итого
        Из общего числа жилой площади находится:
        a) в мансардах б) в мезонинах в) в цокольных этажах г) в подвалах
        Итого
        Распределение квартир по числу комнат (без общежит. и коридорн. сист.)
        Текущие изменения
        № n/n
        Квартиры
        Число
        квар-тир
        Общая площ без учета балк. и подж
        жилая
        об пл.
        пло-щадь число без
        жилая
        Число об пл. без
        квар-тир уч. балки площадь квартир уч. балки лодж.
        жилая
        площадь
        лодж.
        4
        8
        9
        Однокомнатные""",
                """АРХИВ
        МОСКОВСКИЙ
        федеральное агентство
        ф
        кадастра объектов недвижимости
        ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ УНИТАРНОЕ ПРЕДПРИЯТИЕ,
        ОСНОВАННОЕ НА ПРАВЕ ХОЗЯЙСТВЕННОГО ВЕДЕНИЯ,
        "РОССИЙСКИЙ ГОСУДАРСТВЕННЫЙ ЦЕНТР ИНВЕНТАРИЗАЦИИ
        И УЧЕТА ОБЪЕКТОВ НЕДВИЖИМОСТИ - ФЕДЕРАЛЬное бюро технической
        инвентаризации"
        ФГУП "РОСТЕХИНВЕНТАРИЗАЦИЯ - ФЕДЕРАЛЬНОЕ БТИ"
        Московский городской филиал
        технический паспорт
        на
        нежилое здание
        01 Производственный корпус оснастки и инструментабы
        (наименование объекта)
        Адрес (местоположение):
        Субъект Российской Федерации Район
        город Москва Северный административный округ
        Муниципальное образование
        тип
        внутригородская территория города федерального значения
        Населенный пункт
        Улица (проспект, переулок и т.д.)
        наименование тип город наименование Москва тип улица наименование Поликарпова
        Муниципальное образование Хорошевское
        Номер дома Номер корпуса Номер строения Литера Иное описание местоположения
        Адрес объекта
        зарегистрирован реестре зданий сооружении т. Москвы
        Инвентарный номер Реестровый номер Кадастровый номер
        Пас Паспорт составлен по состоянию на
        28 " января 2009 г.
        Руководитель
        B.E. Лопу (Ф.И.О.)
        М.П.
        ГОСТРИСО 9001-2001
        (150 9001 2000)""",
                """ГБУ Московское городское бюро технической инвентаризации
        № квартала
        3488
        Первое территориальное управление
        № дела
        18
        unom
        5046055
        ТЕХНИЧЕСКИЙ ПАСПОРТ ЗДАНИЯ (СТРОЕНИЯ)
        Адрес (иное описание местоположения)
        Субъект Российской Федерации Административный округ Муниципальный округ, поселение Населённый пункт Микрорайон, квартал, иное Улица (пер. , бульв. , просп. и др.)
        дом
        17
        город Москва Юго-Восточный административный округ Выхино-Жулебино
        Сормовский проезд корпус
        строение
        1Б/Н
        Иное описание местоположения
        Наименование
        нежилое
        Кадастровый номер Назначение Функциональное назначение
        нежилое
        Количество проживающих в жилых помещениях
        Регистрация адреса в Адресном реестре объектов недвижимости города Москвы:
        Регистрационный №
        Дата регистрации
        Дата внесения текущих изменений: 18.05.2017 г.
        Дата печати паспорта: 23.06.2017 г.""",
            ],
            "Договор аренды земельного участка": [
                """договор аренды земельного
        предоставляемого правообладателю зданий, строений, сооружений, расположенных на земельном уч делами
        [№ - 7- 303132
        (Номер договора)
        (Число) (Месяц) (Год) 77:07:0006004:108 (Кадастровый №)
        07-01-07472 (Условный №)
        г. Москва
        Департамент городского имущества города Москвы, именуемый в дальнейшем «Арендодатель», в лице заместителя начальника Управления оформления имущественных и земельно-правовых отношений Департамента городского имущества города Москвы Головян Марии Александровны, действующей на основании Положения о Департаменте городского имущества города Москвы и доверенности от «27 201 г. № от имени Правительства Москвы, с одной стороны, и
        Негосударственное образовательное учреждение «Центр развития ребенка детский сад c углубленным изучением языка», именуемое дальнейшем «Арендатор», в лице Директора Никольской Анны-Марии Юрьевны, действующей на основании Устава, с другой стороны, в соответствии с распоряжением Департамента городского имущества города Москвы от 10 декабря 2013 г. № 7021-01 ДГИ, именуемые в дальнейшем «Стороны», заключили настоящий Договор о нижеследующем:
        1. предмет договора и цель предоставления
        земельного участка
        1.1. Предметом Договора является земельный участок, именуемый в дальнейшем «Участок», площадью 4 500 (четыре тысячи пятьсот) кв.м из состава земель населенных пунктов, кадастровый номер 77:07:0006004:108, имеющий адресный ориентир: г.Москва, ул. Пырьева, вл.11А, предоставляемый в пользование на условиях аренды для эксплуатации здания в целях дошкольного
        образования.
        1.2. Передача Участка по настоящему Договору от Арендодателя к
        Арендатору совпадает с моментом возникновения правоотношений по Договору.
        1.3. Установленная в п.1.1 цель предоставления Участка может быть изменена или дополнена на основании распорядительного акта уполномоченного органа власти города Москвы.
        1.4. Границы Участка идентифицированы на прилагаемой к Договору копии кадастрового паспорта земельного участка (Приложение 1), являющейся неотъемлемой частью настоящего Договора.""",
                """правительство москвы
        МОСКОВСКИЙ ЗЕМЕЛЬНЫЙ КОМИТЕТ
        ДОГОВОР
        О ПРЕДОСТАВЛЕНИИ УЧАСТКА
        в пользование на условиях аренды
        (договор аренды земли)
        № М-01-256863
        200 3 г.""",
                """1 экземпляр
        23
        Учетный номер дополнительного соглашения №14-07-003711 от«49 200 года
        дополнительное соглашение к договору аренды земельного участка
        69-
        от 14.12.1995 года №M-07-003711
        Департамент земельных ресурсов города Москвы, именуемый в дальнейшем
        "Арендодатель", в лице начальника Территориального объединения регулирования землепользования Департамента земельных ресурсов города Москвы в Западном административном округе г. Москвы Татарского Георгия Мариновича, действующего на основании Положения от имени Правительства г. Москвы и доверенности от 21.12.2006г. №33-И-3253/1-(6), с одной Стороны, и Открытое акционерное общество "Московский телевизионный завод "Рубль", именуемое в дальнейшем "Арендатор", в лице генерального директора Махана Удраса, действующего на основании Устава и протокола №35 заседания Совета директоров Открытого акционерного общества "Московский телевизионный завод "Рубль" от 12.04.2007 г., с другой Стороны, заключили настоящее дополнительное соглашение о нижеследующем:
        1. На основании обращения Арендатора, распоряжения префекта Западного административного округа города Москвы от 28.06.2007 №731-РП "О внесении изменений в распоряжение префекта от 1 ноября 1994 года №1241-РП "Об установлении права пользования земельным участком акционерному обществу открытого типа Московский телевизионный завод "Рубль" во вл.8 по Багратионовскому проезду", внести изменения в договор аренды земельного участка от 14.12.1995 №M-07-003712.
        2. Пункт 1.1. раздела 1. "Предмет договора и целевое использование земли изложить в
        следующей редакции: "1.1. Предметом договора являются три земельных участка: площадью 69065 кв.м, (кадастровый №77:07:05009:011), площадью 13 кв.м, (кадастровый №77?(Г7У05б69:012(002), являющийся частью 002 земельного участка УДС площадью 13950.77 кв.м. по адресу: г.Москва, Багратионовский проезд (кадастровый №77:07:05009:013), площадью 5 кв.м, (кадастровый №77:07:05009:036(002), являющийся частью 002 земельного участка УДС площадью 27620.75 кв.м. по адресу: г.Москва, ул. Барклая (кадастровый №77:07:05009:037, именуемые в дальнейшем "Участок", общей площадью 69084 (шестьдесят девять тысяч восемьдесят четыре) кв.м., по адресу: г.Москва, Багратионовский проезд, вл.8, предназначенный для дальнейшей эксплуатации здания торгового назначения (2,8944 га), для эксплуатации административных зданий (0.7402 га), для эксплуатации зданий многоэтажных автостоянок (0.9343 га), для эксплуатации открытых автостоянок с благоустройством для посетителей и работников торгового комплекса
        (2.3388 га)."
        3. Считать утратившим силу приложение №1 "Расчет арендной платы" к Договору от 14.12.1995 №M-07-003711. Расчет арендной платы приведен в Приложении №l "Арендная плата" к настоящему дополнительному соглашению.""",
            ],
            "Разрешение на ввод объекта в эксплуатацию": [
                """правительство москвы
        КОМИТЕТ ГОСУДАРСТВЕННОГО СТРОИТЕЛЬНОГО Над ора
        города москвы
        (МОСГОССТРОЙНАДЗОР)
        ул. Брянская, д. 9. Москва, 121059; телефон/факс: (495) 240-03-12; e-mail: info@stroinadzor.ru, http://www.stroinadzor.ru
        регистрационный №77-ГК
        от
        Кому ОАО "Домостроительный комбинат №9
        (наименование застройщика, (фамилия, имя, отчество - для
        Подпись
        119530, г. Москва, проезд. Стройкомбината, граждан, полное наименование организации - для юридических
        Дело № 19656
        владение 7
        лиц). его почтовый индекс и адрес)
        разрешение
        навводобъекта в эксплуатацию
        № RU77176000-002087
        1. Комитет государственного строительного надзора города Москвы, руководствуясь статьей 55 Градостроительного кодекса Российской Федерации, разрешает ввод в эксплуатацию построенного, реконструированного, объекта
        (ненужное зачеркнуть)
        капитального строительства: цех № 5 по изготовлению ограждающих и плоских
        (наименование объекта капитального строительства в соответствии
        элементов на Очаковском заводе ЖБК ОАО ДСК-9 (Ш очередь)
        с проектной документацией)
        расположенного по адресу: 11953.0. г. Москва проезд Стройкомбинатак вл.7
        (полный адрес объекта капитального строительства с указанием субъекта
        стр. 72
        Российской Федерации, административного района и т.д. или строительный адрес)
        строительный адрес: ЗАО. Очаково-Матвеевское проезд Стройкомбината вл.7""",
                """правительство москвы
        КОМИТЕТ ГОСУДАРСТВЕННОГО СТРОИТЕЛЬНОГО НАДзора
        города москвы
        (МОСГОССТРОЙНАДЗОР)
        ул. Брянская, д. 9. Москва, 121059; телефон/факс: (495) 240-03-12: e-mail: info(irstroinadzor.ru, http://www.stroinadzor.ru
        реги
        №77-F1
        Кому
        ЗАО Институт перерабатывающей
        (наименование застройщика, (фамилия, имя, отчество - для
        115093, г. Москва,
        граждан, полное наименование организации - для юридических
        Дело № 21947
        1-й Щипковский пер., д. 91
        лиц). его почтовый индекс и адрес)
        разрешение
        навводобъекта в эксплуатацию
        № RU77130000-001887
        1. Комитет государственного строительного надзора города Москвы, руководствуясь статьей 55 Градостроительного кодекса Российской Федерации, разрешает ввод в эксплуатацию построенного, реконетруированногө, объекта
        (ненужное зачеркнуть)
        капитального строительства: учебный корпус с общежитием гостиничного типа (наименование объекта капитального строительства в соответствии
        с проектной документацией)
        расположенного по адресу: 115093, г. Москва, ул. Щипок, дом 22, стр. 1
        (полный адрес объекта капитального строительства с указанием субъекта
        Российской Федерации, административного района и т.д. или строительный адрес)
        строительный адрес: ЦАО, район Замоскворечье, улица Щипок, вл. 22""",
                """ПРАВИТЕЛЬСТВО МОСКВЫ
        КОМИТЕТ ГОСУДАРСТВЕННОГО СТРОИТЕЛльного надзора
        городамосквы
        (МОСГОССТРОЙНАДЗОР)
        ул. Брянская, д. 9. Москва, 121059; телефон/факс: (495) 240-03-12; e-mail: info@stroinadzor.ru, http://www.stroinadzor.ru
        регистрационный №77-гк/
        Кому ЗАО «Каширский ворон»
        (наименование застройщика, (фамилия, имя, отчество - для
        Подпись
        граждан, полное наименование организации - для юридическ
        Дело № 22565
        115201, г. Москва, Старокаширское шоссе, д. 12, корп. 4
        лиц) его почтовый индекс и адрес)
        разрешение
        на вводобъекта в эксплуатацию
        № RU77163000-002043
        1. Комитет государственного строительного надзора города Москвы, руководствуясь статьей 55 Градостроительного кодекса Российской Федерации, разрешает ввод в эксплуатацию построенного, реконструированного, объекта
        (ненужное зачеркнуть)
        капитального строительства: торгово-складской комплекс
        (наименование объекта капитального строительства в соответствии
        с проектной документацией)
        расположенного по адресу: 115230, г. Москва, Каширское шоссе, дом 19, корп. 2
        (полный адрес объекта капитального строительства с указанием субъекта
        Российской Федерации, административного района и т.д. или строительный адрес)
        строительный адрес: ЮАО, Нагатино-Садовники, пересечение Каширского
        шоссе и Коломенского проезда""",
            ],
            'Разрешение на строительство': [
                """правительство москвы
        КОМИТЕТ ГОСУДАРСТВЕННОГО СТРОИТтельного надзора
        городамосквы
        (МОСГОССТРОЙНАДЗОР)
        ул. Брянская, д. 9. Москва, 121059; телефон/факс: (495) 240-03-12; e-mail: info@stroinadzor.ru, http://www.stroinadzor.ru
        ОКПО 40150382, ОГРН 1067746784390, ИНН/КПП 7730544207/773001001
        Дело № 24008
        экз. № 1
        Кому:
        ГУП "Московская городская служба
        технического
        (наименование застройщика (фамилия, имя, отчество - для граждан, полное наименование организации
        для юрилических лиц)
        107076 Москва Краснобогатырская дом 7 корп. 2 А, тел. 964-16-10
        ИНН/КПП 77181228 П71801С
        ( его почтовый индекс и адрес)
        разрешение И регистрационный
        на строительство №
        № RU77169000-004924
        от
        Под
        Комитет государственного строительного надзора города Москвы
        (наименование уполномоченного федерального органа исполнительной власти, или органа исполнительной власти субъекта Российской Федерации, или органа местного
        самоуправления, осуществляющих выдачу разрешения на строительство)
        руководствуясь статьей 51 Градостроительного кодекса Российской Федерации, разрешает:
        строительство, реконструкцию, капитальный ремонт объекта капитального строительства,
        (ненужное зачеркнуть)
        пункт государственного технического осмотра автомобилей
        ( наименование объекта капитального строительства в соответствии с проектной документацией,
        Общая площадь
        Площадь
        68,6
        (кв.м):
        участка (га):
        в том числе
        Объем (куб. м): 3510,1
        подземной
        части (куб. м):
        Сметная стоимость объекта капитального
        строительства (тыс, руб. ) (в базисных
        ценах 1998 г.)
        0,22
        Количество
        этажей:
        1+антресоль
        Количество мест хранения автомобилей (маш. -мест):
        Удельная стоимость кв.м площади
        (тыс. руб. ):
        Верхняя
        м):
        9,07
        отметка (м):
        краткие проектные характеристики,
        описание этапа строительства, реконструкции, если разрешение выдается на этап строительства, реконструкции)
        расположенного по адресу: г. Москва, ВАО, Проектируемый проезд N 3
        (полный адрес объекта капитального строительства с указанием субъекта Российской Федерации, административного района и т. д. или строительный адрес)
        Срок действия настоящего разрешения - до
        «7» февраля 2011 г.
        Первый заместитель
        председателя
        (довжибет, уполномоченного
        оргімі, выдачу разрешения
        Дльство),
        B.H.
        (расшифровка подписи)
        « 7 »мая 2010 г.
        М.П.""",
                '''правительство москвы
        КОМИТЕТ ГОСУДАРСТВЕННОГО СТРОИТЕЛЬНОГО НАдзора
        города москвы
        (МОСГОССТРОЙНАДЗОР)
        ул. Брянская, д. 9. Москва, 121059; телефон/факс: (499) 240-03-12; e-mail: info@stroinadzor.ru, http://www.stroinadzor.ru
        ОКПО 40150382, ОГРН 1067746784390, ИНН/КПП 7730544207/773001001
        Дело № 24455
        экз. № 1
        Кому:
        ООО "ФИРМА К.С.К.
        (наименование застройщика (фамилия, имя, отчество - для граждан, полное наименование органи зации
        для юридических лиц)
        107082 Москва, Спартаковская площадь дом | стр. I, тел. 662-57-10
        ИНН/КПП 7701176012/770101001
        ( его почтовый индекс и адрес)
        Разрешение И регистрационный
        на строительство
        №
        № RU77203000-005444
        от
        Д Поді
        Комитет государственного строительного надзора города Москвы
        (наименование уполномоченного федерального органа исполнительной власти, или органа исполнительной власти субъекта Российской Федерации, или органа местного
        самоуправления, осуществляющих выдачу разрешения на строительство)
        руководствуясь статьей 51 Градостроительного кодекса Российской Федерации, разрешает:
        строительство, реконструкцию, капитальный ремонт объекта капитального строительства,
        (ненужное зачеркнуть)
        многофункциональный комплекс с подземной автостоянкой
        ( наименование объекта капитального строительства в соответствии с проектной документацией,
        Общая площадь
        (кв.м):
        Объем (куб. м):
        Площадь
        25000
        участка
        (га
        (га):
        в том числе
        подземной
        части
        (куб. м):
        36900,0
        0,13
        9833,4
        9700,0
        Количество
        этажей:
        6-9+
        2 подз. ур. (м):
        подземной автостоянки
        вместимостью 62 м/места (кв.мл
        Площадь застройки (кв м)
        Верхняя
        отметка
        29,0
        1982,7
        82,
        Сметная стоимость объекта капитального
        строительства (тыс. руб. ) (в базисных
        ценах 1998 г.):
        Удельная стоимость
        площади (тыс. руб.
        краткие проектные характеристики,
        описание этапа строительства, реконструкции, если разрешение выдается на этап строите
        расположенного по адресу: г. Москва, ЦАО, Большой Каретный переулок, в
        (полный адрес объекта капитального строительства с указанием субъекта Российской Федерации, административного района и т. д. Или стройтельный адрес)
        Срок действия настоящего разрешения - до «31 » декабря 2011 г.
        Первый заместителе
        председателя
        B. Н. Африн
        (должность уполномоченного сотрудни
        органа, осуществляющего выдачу разре
        на строительство)
        (расшифровка подписи)
        « 13 » сентября 2010 г.
        М.П.
        ЗАО фирма "ЭПО", г. Москва, з.774, 2010 г., уровень В"''',
                """правительство москвы
        КОМИТЕТ ГОСУДАРСТВЕННОГО СТРОИТЕЛльного надзора
        городамосквы
        (МОСГОССТРОЙНАДЗОР)
        ул. Брянская,
        9. Москва, 121059, телефонфакс: (109) 240 03 12 mail mforastroinadzorm, http: //www.stopinadzor
        ОКПО 40150382, ОГРН 1067746784390, ИНН/КПП 7730544207/773001001
        Дело № 24453
        экз. № 1
        Кому:
        ЗАО "Мосрыб)
        (наименование застройщика (фамилия, имя, отчество - для граждан, полное наименование организации
        для юридических лиц)
        123001, Москва, Ермолаевский переулок, д. 22 , стр. 1, тел. 609-08-5
        ИНН/КПП 77070542 (7749010
        (его почтовый индекс и адрес)
        разрешение
        на строительство
        И регистрационный
        №
        № RU77104000-005299
        от
        Комитет государственного строительного надзора города Москвы
        (наименование уполномоченного федерального органа исполнительной власти, или органа исполнительной власти субъекта Российской Федерацин, или органа местного
        самоуправления, осуществляющих выдачу разрешения на строительство)
        руководствуясь. статьей 51 Градостроительного кодекса Российской Федерации, разрешает:
        строительство, реконструкция, капитальный ремонт объекта капитального строительства,
        (ненужное зачеркнуть)
        Многофункциональный комплекс с подземной автостоянкой
        ( наименование объекта капитального строительства в соответствии с проектной документацией,
        Общая площадь
        (кв.м):
        Объем (куб. м):
        311,40 Площадь
        участка (га):
        в том числе
        подземной части
        (куб. м):
        0,82
        Количество
        этажей:
        3-6+
        4подз. (м):
        Верхняя
        отметка
        22,90
        Площадь застройки (кв.м): 134,0
        Площадь автостоянки на 421 м/мест (кв.м): 15109.25
        Сметная стоимость объекта капитального
        строительства (тыс. руб. ) (в базисных
        ценах 1998 г.):
        краткие проектные характеристики,
        Удельная стоимость 1 кв.м
        площади (тыс. руб. ):
        описание этапа строительства, реконструкции, если разрешение выдается на этап строительства, реконструкции)
        расположенного по адресу: г. Москва, ЦАО, Поварская улица, вл. 7/13/1, стр. 1,2 , вл.11,
        Хлебный пер. вл.4
        (полный адрес объекта капитального строительства с указанием субъекта Российской Федерации, административного района и т. д. кли стронтельный адрес)
        Срок действия настоящего разрешения - до «10» апреля 2015 г.
        (должны
        орган выдачу
        на строительство)
        председателя
        А.Б. Пирров
        (расшифровка подписи)
        ЗАО фирма "ЭПО". г. Москва, з.774, 2010 г., уровень "В"""
            ],
            'Свидетельство АГР': [
                """ПРАВИТЕЛЬСТВО МОСКВЫ
        КОМИТЕТ ПО АРХИТЕКТУРЕ И ГРАДОСТРОИТЕЛЬСТВУ Г. МОСКВЫ
        125047, Москва, Триумфальная площадь,1
        тел. 250-55-20
        Код объекта недвижимости:
        Главный архитектор города
        Код строительного объекта:
        Регистрационный №:
        841-61/151-22
        80-3/3-02
        a.Д.
        Кутемин
        СВИДЕТЕЛЬСТВО ОБ УТВЕРЖДЕНИИ
        архитектурно-градостроительного решения
        АДРЕС ОБЪЕКТА:
        Город:
        Москва
        Административный округ
        Центральный
        Район:
        Якиманка
        Адрес:
        улица Большая Полянка
        Владение:
        5г
        Корпус:
        Строение:
        Наименование объекта:
        Проект реконструкции административного здания
        с пристройками
        Функциональное
        назначение объекта:
        Заказчик:
        Многофункциональный комплекс
        ООО
        "АКС
        Проект"
        Застройщик:
        ООО "АС СТРОЙ"
        Разрешение на проектирование:
        Распоряжение Правительства Москвы
        от 23.01.2003г. №8-РП
        АВТОРСКИЙ КОЛЛЕКТИВ
        Руководитель авторов
        проекта
        Оразов С.А.
        Авторы проекта:
        Оразов С.А., Демиденко А.С., Мишалко Д.Н.
        Проектная организация:
        ООО "АСЦ Диоген"
        СОГЛАСОВАННЫЕ ТЕХНИКО-ЭКОНОМИЧЕСКИЕ ПОКАЗАТЕЛИ ПО ОБЪЕКТУ
        Площадь
        застройки(м2):
        550. 0
        Объем (м3)
        (м?:
        7 600. 0
        Этажность:
        3-4
        Верхняя
        отметка объекта
        16.65
        (max) (м):
        Общая площадь(м2):
        2 668. 0
        В том числе:
        наземная (м2):
        2 668. 0
        подземная (м2):
        natalia""",
                """ВЫПИСКА ИЗ ПРОТОКОЛА
        Регламента рассмотрения проектных решений
        Главным архитектором г. Москвы
        дата:
        25.09.01
        30
        пункт:
        119
        Наименование объекта:
        ТЭО (проект) строительства объекта складирования жидких
        Авторы проекта:
        противогололедных реагентов
        Кокнев В.Г., Скрытников ТВ.
        Генеральная проектная
        организация:
        Застройщик:
        ГУП им. К.Д. Парилова
        Управление жилищно-дорожного хозяйства
        ВАО г. Москвы
        Рассмотрение на рабочей комиссии
        Референт:
        Попов В.П.
        Докладчик:
        Выступили:
        ПОСТАНОВИЛИ:
        1. Одобрить представленное архитектурно-градостроительное решение.
        Председатель архитектурного
        совета:
        Кутемин А.В.
        Ученый секретарь
        архитектурного совета:
        "ВЫПИСКА ИЗ ПРОТОКОЛА ВЕРНА"
        Начальник Управления Архитектурного совета:
        Кудряшов СП.
        Начальник Управления подготовки
        согласования проектов:
        Судепов А. И.
        Руководитель авторов проекта:
        Кокнев В.Г.
        ПРИЛОЖЕНИЯ:
        Материалы проектного решения (формата А4, без
        ситуационный план, генплан, планы этажей, разрезы, фасады
        с цветовым решением.
        Верно:""",
                """ПРАВИТЕЛЬСТВО МОСКВЫ
        КОМИТЕТ ПО АРХИТЕКТУРЕ И ГРАДОСТРОИТЕЛЬСТВУ Г. МОСКВЫ
        125047, Москва, Триумфальная площадь,1
        Код объекта недвижимости:
        тел. 250-55-20
        Главный архитектор города
        Код строительного объекта:
        01-424-200/3
        A.B. Кутемин
        Регистрационный №;
        2/97-14-073
        СВИДЕТЕЛЬСТВО ОБ УТВЕРЖДЕНИИ
        архитектурно-градостроительного решения
        АДРЕС ОБЪЕКТА:
        Город:
        Москва
        Административный округ
        Юго-Западный
        Район:
        Академический
        Адрес:
        улица Вавилова
        Владение:
        17Г
        Корпус:
        Строение:
        Наименование объекта:
        Проект строительства административного здания
        Функциональное
        назначение объекта:
        Административное здание
        Заказчик:
        Застройщик:
        ООО
        ООО
        "Загранкомплекс"
        "Загранкомплекс"
        Разрешение на проектирование:
        Решение комиссии по предоставлению земельных участков и
        градостроительному регулированию ЮЗАО г. Москвы.
        Протокол №1 от 11.08.2003г.
        АВТОРСКИЙ КОЛЛЕКТИВ
        Руководитель авторов
        проекта
        Ходай К.В.
        Авторы проекта:
        Ходай К.В., Ларцов Д.В., Сидоренко Н.В., Бескроватный Ю.Л.
        Проектная организация:
        ЗАО "ТристаН"
        СОГЛАСОВАННЫЕ ТЕХНИКО-ЭКОНОМИЧЕСКИЕ ПОКАЗАТЕЛИ ПО ОБЪЕКТУ
        Площадь
        застройки(м2):
        1 100. 0
        Объем (м3):
        16 574. 0
        Этажность:
        Верхняя
        отметка объекта
        18.60
        (max) (м):
        Общая площадь(м2):
        5 185. 0
        В том числе:
        наземная (м2):
        3 387. 0
        подземная (м2):
        798. 0""",
                """ВЫПИСКА ИЗ ПРОТОКОЛА
        Регламента рассмотрения проектных решений
        Главным архитектором г. Москвы
        дата:
        22.02.99
        №:
        пункт:
        56
        Наименование объекта:
        ТЭО строительства мусороперегрузочного комплекса по
        утилизации твердых
        бытовых отходов
        Авторы проекта:
        Кистенев Л.Г., Замокина А.В.
        Генеральная проектная
        организация:
        Застройщик:
        ОАО "Интмашпроч" 1"
        ОАО "ДК-Строй"
        Рассмотрение на рабочей комиссии
        Референт:
        Карпов П.М.
        Докладчик:
        Выступили:
        постановили:
        1. Одобрить переработанные архитектурно-планировочные решения.
        2.Скорректированное ТЭО направить в УПСП МКА для оформления согласования в
        установленном порядке.
        Председатель архитектурного
        совета:
        Кутемин А.В.
        Ученый секретарь
        архитектурного совета:
        "выписка из протокола верна"
        Начальник Управления Архитектурного совета:
        Кудрявев СП.
        Начальник Управления подготовки
        согласования проектов:
        СудеповА.И.
        Руководитель авторов проекта:
        Кистенев Л.Г.
        ПРИЛОЖЕНИЯ:
        Материалы проектного решения (формата А4, без масштаба):
        ситуационный план, генплан, планы этажей, разрезы, фасады
        с цветовым решением.
        Верно:""",
                """125047, Москва, Триумфальная площадь,1
        ПРАВИТЕЛЬСТВО МОСКВЫ
        КОМИТЕТ ПО АРХИТЕКТУРЕ И ГРАДОСТРОИТЕЛЬСТВУ
        тел. 250-55-20
        Код объекта недвижимости:
        Главный архитектор города
        Код строительного объекта:
        014-311-2052
        A. B.
        Кутемин
        Регистрационный №;
        20-52-4/03
        8 ы
        СВИДЕТЕЛЬСТВО ОБ УТВЕРЖДЕНИИ
        архитектурно-градостроительного решения
        АДРЕС ОБЪЕКТА:
        Город:
        Москва
        Административный округ
        Северо-Западный
        Район:
        Куркино
        Адрес:
        Новокуркинское шоссе
        Владение:
        Корпус:
        Строение:
        Наименование объекта:
        Рабочий проект строительства тяговой подстанции №5
        Функциональное
        назначение объекта:
        Заказчик:
        Застройщик:
        Тяговая подстанция
        ОАО "Мосинфострой"
        ОАО "Мосинфострой"
        Разрешение на проектирование:
        Постановление Правительства Москвы от 15.12.99г. №989
        АВТОРСКИЙ КОЛЛЕКТИВ
        Руководитель авторов
        проекта
        Троцкий СВ.
        Авторы проекта:
        Троцкий СВ., Лазарева К.П.
        Проектная организация:
        ЗАО "Промавтопроект"
        СОГЛАСОВАННЫЕ ТЕХНИКО-ЭКОНОМИЧЕСКИЕ ПОКАЗАТЕЛИ ПО ОБЪЕКТУ
        Площадь
        застройки(м?)
        635. 0
        Объявления
        Объем (м
        6 900. 0
        Этажность:
        2
        Верхняя
        отметка объекта
        (max) (м):
        11.22
        Общая площадь(м2):
        1 635. 0
        В том числе:
        наземная (м'):
        1 635. 0
        подземная (м2):""",
                """ВЫПИСКА ИЗ ПРОТОКОЛА
        Регламента рассмотрения проектных решений
        Главным архитектором г. Москвы
        дата:
        10.02.03
        пункт:
        48
        Наименование объекта:
        Рабочий проект строительства тяговой подстанции №5
        Авторы проекта:
        Генеральная проектная
        организация:
        Застройщик:
        Троцкий СВ., Лазарева К.П.
        ЗАО "Промавтопроект"
        ОАО "Мосинфострой"
        Рассмотрение на рабочей комиссии
        Референт:
        Петров В.П.
        Докладчик:
        Выступили:
        постановили:
        1. Одобрить представленное архитектурно-градостроительное решение.
        Председатель архитектурного
        совета:
        Кутемин А.В.
        Ученый секретарь
        архитектурного совета:
        "выписка из протокола верна"
        Начальник Управления Архитектурного совета:
        Кудряшов СП.
        Начальник Управления подготовки
        согласования проектов:
        Куренный А.М.
        Руководитель авторов проекта:
        Троцкий СВ.
        ПРИЛОЖЕНИЯ:
        Материалы проектного решения (формата А4 без масштаба):
        ситуационный план, генплан, планы этажей, разрезы, фасады
        с цветовым решением.
        Верно:"""
            ],
        }
        print(d.keys())
        # data = PageDocument.objects.filter(page=1).values('parent_document__file_type', 'ocr_text').distinct()
        # c = PageDocument.objects.filter(page=1)
        # print(c.count())

        data = []
        for k, v in d.items():
            for t in v:
                data.append({'label': k, 'text': t})

        df = pd.DataFrame(data)
        print(df)
        # df['ocr_text'] = df['ocr_text'].apply(lambda x: x.replace('\n', ' ') if x else '')
        df.to_csv('dataset.csv')