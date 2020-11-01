from django.core.management import BaseCommand
from ocr.models import DocumentType


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Скрипт заполнения базы типами файлов."""
        doc_types_and_attrs = {
            'Свидетельство об утверждении архитектурно-градостроительного решения': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'issuing_authority': {
                    'description': 'Выдавший орган',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
                'administrative_district': {
                    'description': 'Административный округ',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
                'district': {
                    'description': 'Район',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
                'address': {
                    'description': 'Адрес',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'object_name': {
                    'description': 'Наименование объекта',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'object_functional_purpose': {
                    'description': 'Функциональное назначение объекта',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'built_up_area': {
                    'description': 'Площадь застройки',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'volume': {
                    'description': 'Объем',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'floors_number': {
                    'description': 'Этажность',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'object_top_elevation': {
                    'description': 'Верхняя отметка объекта',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'total_area': {
                    'description': 'Общая площадь',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'including_overground_area': {
                    'description': 'В том числе надземная площадь',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'underground_area': {
                    'description': 'Подземная площадь',
                    'type': 'text',
                    'section': '',
                    'choices': []
                }
            },
            'Технический паспорт (МосгорБТИ, МособлБТИ,  Ростехинвентаризация, ВИСХАГИ)': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'issuing_authority': {
                    'description': 'Выдавший орган',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
                'documentation_source': {
                    'description': 'Источник документации',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'document_filling_date': {
                    'description': 'Дата заполнения документа',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'object_name': {
                    'description': 'Наименование объекта',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'inventory_number': {
                    'description': 'Инвентарный номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'main_characteristic_value': {
                    'description': 'Значение основной характеристики',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'year_built': {
                    'description': 'Год постройки',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'commissioning_year': {
                    'description': 'Год ввода в эксплуатацию',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'land_plot_cadastral_number': {
                    'description': 'Кадастровый номер ЗУ',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'cadastral_number': {
                    'description': 'Кадастровый номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'building_plan_stamp_recognition': {
                    'description': 'Распознавание штампа планов зданий',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date_stamp_filling': {
                    'description': 'Дата заполнения штампа, ',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'changes_dates': {
                    'description': 'Даты внесения изменений',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'owners_name': {
                    'description': 'Наименование владельцев',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'object_composition': {
                    'description': 'Состав объекта',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'name': {
                    'description': 'Наименование',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'square': {
                    'description': 'Площадь',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'land_plot_explication': {
                    'description': 'Экспликация на земельный участок',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'target_landmark': {
                    'description': 'Адресный ориентир',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'appointment': {
                    'description': 'Назначение',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'survey_marks': {
                    'description': 'Отметки об обследованиях',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
            },
            'Технический паспорт на здание': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'issuing_authority': {
                    'description': 'Выдавший орган',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
                'object_purpose': {
                    'description': 'Назначение объекта',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'address': {
                    'description': 'Адрес',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'owner': {
                    'description': 'Владелец',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'year_built': {
                    'description': 'Год постройки',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'floors_number': {
                    'description': 'Число этажей',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'basement': {
                    'description': 'Подвал',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'technical_underground': {
                    'description': 'Тех. подполье',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'ground_floor': {
                    'description': 'Цокольный этаж',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'attic': {
                    'description': 'Мансарда',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'mezzanine': {
                    'description': 'Мезонин',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'roof_area': {
                    'description': 'Площадь крыши',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'volume': {
                    'description': 'Объем',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'building_total area': {
                    'description': 'Общая площадь по зданию. В т.ч. общей без учета балконов и лоджий',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'total_living_space': {
                    'description': 'Общая площадь жилых помещений. В т.ч. общая площадь без учёта балконов и лоджий',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'total_area_remaining_to_the_common_property_of_the_condominium': {
                    'description': 'Общая площадь, остающаяся к общему имуществу кондоминиума',
                    'type': 'text',
                    'section': '',
                    'choices': []
                }
            },
            'Технический паспорт на домовладение (земельный участок)': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'issuing_authority': {
                    'description': 'Выдавший орган',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
                'technical_passport_preparation_date': {
                    'description': 'Дата составления технического паспорта',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'entry_date': {
                    'description': 'Дата записи',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'building_owner_name': {
                    'description': 'Наименование владельца здания (площадь права по документу)',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'ownership_basis': {
                    'description': 'Основание владения (дата и номер документа)',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'building_number': {
                    'description': 'Номер строения',
                    'type': 'text',
                    'section': 'Основные экономические показатели строений в домовладении',
                    'choices': []
                },
                'building_purpose': {
                    'description': 'Назначение строения',
                    'type': 'text',
                    'section': 'Основные экономические показатели строений в домовладении',
                    'choices': []
                },
                'wall_material': {
                    'description': 'Материал стен',
                    'type': 'text',
                    'section': 'Основные экономические показатели строений в домовладении',
                    'choices': []
                },
                'roof_material': {
                    'description': 'Материал крыши',
                    'type': 'text',
                    'section': 'Основные экономические показатели строений в домовладении',
                    'choices': []
                },
                'roof_area': {
                    'description': 'Площадь крыши',
                    'type': 'text',
                    'section': 'Основные экономические показатели строений в домовладении',
                    'choices': []
                },
                'floors_number': {
                    'description': 'Число этажей',
                    'type': 'text',
                    'section': 'Основные экономические показатели строений в домовладении',
                    'choices': []
                },
                'building_area_by_external_measurement': {
                    'description': 'Площадь строения по наружному обмеру в кв.м.',
                    'type': 'text',
                    'section': 'Основные экономические показатели строений в домовладении',
                    'choices': []
                },
                'building_height': {
                    'description': 'Строительная высота',
                    'type': 'text',
                    'section': 'Основные экономические показатели строений в домовладении',
                    'choices': []
                },
                'volume_cubic_meters': {
                    'description': 'Объем (куб.м.)',
                    'type': 'text',
                    'section': 'Основные экономические показатели строений в домовладении',
                    'choices': []
                },
                'dates_of_changes': {
                    'description': 'Даты внесения изменений',
                    'type': 'text',
                    'section': 'Основные экономические показатели строений в домовладении',
                    'choices': []
                }
            },
            'Кадастровый паспорт': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'issuing_authority': {
                    'description': 'Выдавший орган',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
                'cadastral_number': {
                    'description': 'Кадастровый номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'inventory_number': {
                    'description': 'Инвентарный номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'desc': {
                    'description': 'Описание',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'name': {
                    'description': 'Наименование',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'appointment': {
                    'description': 'Назначение',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'address': {
                    'description': 'Адрес',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'location': {
                    'description': 'Местоположение',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'main_characteristic': {
                    'description': 'Основная характеристика',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'land_plot_cadastral_number': {
                    'description': 'Кадастровый номер ЗУ',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'previous_numbers': {
                    'description': 'Предыдущие номера',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'notes': {
                    'description': 'Примечания',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'situational_plan': {
                    'description': 'Ситуационный план',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'scale': {
                    'description': 'Масштаб',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'signed': {
                    'description': 'Подписал',
                    'type': 'text',
                    'section': '',
                    'choices': []
                }
            },
            'Экспликация к архивному поэтажному плану': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'issuing_authority': {
                    'description': 'Выдавший орган',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
                'building_address': {
                    'description': 'Адрес здания',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'floor': {
                    'description': 'Этаж',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'premises': {
                    'description': 'Помещение',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'room_area': {
                    'description': 'Площадь помещения',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'total_floor_area': {
                    'description': 'Общая площадь по этажу',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'total_building_area': {
                    'description': 'Общая площадь здания',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'building_height': {
                    'description': 'Высотность здания',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'floor_plan_date': {
                    'description': 'Дата составления поэтажного плана',
                    'type': 'date',
                    'section': '',
                    'choices': []
                }
            },
            'Договор аренды земельного участка': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'issuing_authority': {
                    'description': 'Выдавший орган',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
                'square': {
                    'description': 'Площадь',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'subject_of_a_contract': {
                    'description': 'Предмет договора',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'purpose_of_the_land_plot': {
                    'description': 'Целевое назначение земельного участка',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'Lease_term': {
                    'description': 'Срок действия договора аренды',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'special_conditions': {
                    'description': 'Особые условия',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'business_entities': {
                    'description': 'Хозяйствующие субъекты',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
            },
            'Плановое (реставрационное) задание': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'object': {
                    'description': 'Выдавший орган',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
                'address': {
                    'description': 'Адрес',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'basis_for_issuing': {
                    'description': 'Основание для выдачи задания',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'brief_historical': {
                    'description': 'Краткие исторические сведения',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'planned_work': {
                    'description': 'Характер планируемых работ',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'situational_plan': {
                    'description': 'Ситуационный план',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
            },
            'Разрешение на производство подготовительных и основных строительно-монтажных работ': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'issuing_authority': {
                    'description': 'Выдавший орган',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
                'construction_address': {
                    'description': 'Адрес строительства объекта',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'name': {
                    'description': 'Наименование объекта',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'resolution': {
                    'description': 'Разрешение',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'validity_period': {
                    'description': 'Срок действия разрешения ',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
            },
            'Заключение Могосэкспертизы': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'object_address': {
                    'description': 'Адрес объекта экспертизы',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'feasibility_study': {
                    'description': 'Технико-экономическое обоснование',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'number_of_floors': {
                    'description': 'Количество этажей',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'built_up_area': {
                    'description': 'Площадь застройки',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'building_volume': {
                    'description': 'Объем здания',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'effective_area': {
                    'description': 'Полезная площадь',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'working_area': {
                    'description': 'Рабочая площадь',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'general_conclusion': {
                    'description': 'Общий вывод по объекту',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
            },
            'Договор': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'line_number': {
                    'description': 'номер строки спецификации',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'name_of_product': {
                    'description': 'наименование товара',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'country_of_origin': {
                    'description': 'страна происхождения',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'unit': {
                    'description': 'единица измерения',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'qty': {
                    'description': 'количество',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'vat': {
                    'description': 'ставка НДС (НДФЛ), %',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'pcs_price': {
                    'description': 'цена за единицу, руб',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'price_total': {
                    'description': 'общая стоимость, руб',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
            },
            'Градостроительное заключение': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'land_area': {
                    'description': 'Площадь участка',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'storeys': {
                    'description': 'Этажность',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'wall_material': {
                    'description': 'Материал стен',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'year': {
                    'description': 'год постройки',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'issuing_authority': {
                    'description': 'Выдавший орган',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'total_area': {
                    'description': 'Общая площадь',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },

            },
            'Акт государственной приемочной комиссии о приемке в эксплуатацию законченного строительством объекта': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'issuing_authority': {
                    'description': 'Выдавший орган',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
                'address': {
                    'description': 'Адрес',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'work': {
                    'description': 'Тип работ',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'indicators': {
                    'description': 'Показатели объекта',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'area': {
                    'description': 'Площадь объекта',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'floors': {
                    'description': 'Этажность',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'volume': {
                    'description': 'Общий строительный объем',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'sections': {
                    'description': 'Количество секций',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
            },
            'Распоряжение префекта': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'issuing_authority': {
                    'description': 'Выдавший орган',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
            },
            'Разрешение на строительство': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'issuing_authority': {
                    'description': 'Выдавший орган',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
                'address': {
                    'description': 'Расположенного по адресу',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'b_address': {
                    'description': 'Строительный адрес',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'b_type': {
                    'description': 'Вид строительства',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'b_object': {
                    'description': 'Объект капитального строительства',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'validity': {
                    'description': 'Срок действия документа',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                't_volume': {
                    'description': 'Общая площадь',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'volume': {
                    'description': 'Объем',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'height': {
                    'description': 'Высота',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                't_square': {
                    'description': 'Площадь застройки',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'buil_square': {
                    'description': 'Площадь участка',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'floors': {
                    'description': 'Количества этажей',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'und_floors': {
                    'description': 'Количество подземных этажей',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'others': {
                    'description': 'Иные показатели',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
            },
            'Разрешение на производство строительно-монтажных работ': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'issuing_authority': {
                    'description': 'Выдавший орган',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
                'address': {
                    'description': 'Адрес строительства объекта',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'district': {
                    'description': 'Административный округ',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'region_inside_mow': {
                    'description': 'Район города Москвы',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'buil_type': {
                    'description': 'Вид строительства',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'validity': {
                    'description': 'Срок действия документа',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
            },
            'Разрешение на ввод объекта в эксплуатацию': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': 'Объекта капитального строительства',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': 'Объекта капитального строительства',
                    'choices': []
                },
                'issuing_authority': {
                    'description': 'Выдавший орган',
                    'type': 'choices',
                    'section': 'Объекта капитального строительства',
                    'choices': []
                },
                'address': {
                    'description': 'Расположенного по адресу',
                    'type': 'text',
                    'section': 'Объекта капитального строительства',
                    'choices': []
                },
                'b_address': {
                    'description': 'Строительный адрес',
                    'type': 'text',
                    'section': 'Объекта капитального строительства',
                    'choices': []
                },
                'b_info': {
                    'description': 'Сведения об объекте капитального строительства',
                    'type': 'text',
                    'section': 'Объекта капитального строительства',
                    'choices': []
                },
                'b_volume': {
                    'description': 'Строительный объем',
                    'type': 'text',
                    'section': 'Объекта капитального строительства',
                    'choices': []
                },
                'incl_aboveground': {
                    'description': 'В том числе надземной',
                    'type': 'text',
                    'section': 'Объекта капитального строительства',
                    'choices': []
                },
                'total_square': {
                    'description': 'Общая площадь',
                    'type': 'text',
                    'section': 'Объекта капитального строительства',
                    'choices': []
                },
                'vent_square': {
                    'description': 'Площадь встроенно-пристроенных помещений',
                    'type': 'text',
                    'section': 'Объекта капитального строительства',
                    'choices': []
                },
                'build_qty': {
                    'description': 'Количество зданий',
                    'type': 'text',
                    'section': 'Объекта капитального строительства',
                    'choices': []
                },

                'Non_production-facilities': {
                    'description': 'Объекты непроизводственного назначения',
                    'type': 'text',
                    'section': 'Нежилые объекты',
                    'choices': []
                },
                'place_qty': {
                    'description': 'Количество мест',
                    'type': 'text',
                    'section': 'Нежилые объекты',
                    'choices': []
                },
                'visits_qty': {
                    'description': 'Количество посещений',
                    'type': 'text',
                    'section': 'Нежилые объекты',
                    'choices': []
                },
                'Capacity': {
                    'description': 'Вместимость ',
                    'type': 'text',
                    'section': 'Нежилые объекты',
                    'choices': []
                },
                'parking_area': {
                    'description': 'Общая площадь подземной автостоянки',
                    'type': 'text',
                    'section': 'Нежилые объекты',
                    'choices': []
                },
                'adm_square': {
                    'description': 'Общая площадь административных помещений ',
                    'type': 'text',
                    'section': 'Нежилые объекты',
                    'choices': []
                },
                'premises_for_cultural': {
                    'description': 'Общая площадь помещений культурно-досугового назначения',
                    'type': 'text',
                    'section': 'Нежилые объекты',
                    'choices': []
                },
                'trade_area': {
                    'description': 'Торговая площадь',
                    'type': 'text',
                    'section': 'Нежилые объекты',
                    'choices': []
                },
                'power': {
                    'description': 'Мощность',
                    'type': 'text',
                    'section': 'Объекты производственного назначения',
                    'choices': []
                },
                'length': {
                    'description': 'Протяженность',
                    'type': 'text',
                    'section': 'Объекты производственного назначения',
                    'choices': []
                },
                'area': {
                    'description': 'Площадь',
                    'type': 'text',
                    'section': 'Объекты производственного назначения',
                    'choices': []
                },
                'cultural_and_leisure': {
                    'description': 'Площадь помещений культурно-досугового',
                    'type': 'text',
                    'section': 'Объекты производственного назначения',
                    'choices': []
                },
                'trade_area2': {
                    'description': 'Торговая площадь',
                    'type': 'text',
                    'section': 'Объекты производственного назначения',
                    'choices': []
                },
                'floors': {
                    'description': 'Этажность',
                    'type': 'text',
                    'section': 'Объекты производственного назначения',
                    'choices': []
                },
                'liv_area': {
                    'description': 'Площадь жилых помещений',
                    'type': 'text',
                    'section': 'Объекты жилищного строительства',
                    'choices': []
                },
                'floors_2': {
                    'description': 'Количество этажей',
                    'type': 'text',
                    'section': 'Объекты жилищного строительства',
                    'choices': []
                },
                'sections_q': {
                    'description': 'Количество секций',
                    'type': 'text',
                    'section': 'Объекты жилищного строительства',
                    'choices': []
                },
                'flats': {
                    'description': 'Количество квартир',
                    'type': 'text',
                    'section': 'Объекты жилищного строительства',
                    'choices': []
                },
            },
            'Выписка из реестра Федерального имущества': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'issuing_authority': {
                    'description': 'Выдавший орган',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
            },
            'Свидетельство о регистрации права': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'issuing_authority': {
                    'description': 'Выдавший орган',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
            },
            'Распоряжение': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'issuing_authority': {
                    'description': 'Выдавший орган',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
            },
            'Определение': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'issuing_authority': {
                    'description': 'Выдавший орган',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
            },
            'Акт': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'issuing_authority': {
                    'description': 'Выдавший орган',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
            },
            'Разрешение': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'issuing_authority': {
                    'description': 'Выдавший орган',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
            },
            'Заключение': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'issuing_authority': {
                    'description': 'Выдавший орган',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
            },
            'Проект': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'issuing_authority': {
                    'description': 'Выдавший орган',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
            },
            'Письмо': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'issuing_authority': {
                    'description': 'Выдавший орган',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
            },
            'Пояснительная записка': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'issuing_authority': {
                    'description': 'Выдавший орган',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
            },
            'Поэтажный план': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'issuing_authority': {
                    'description': 'Выдавший орган',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
            },
            'Выписка из ЕГРН': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'issuing_authority': {
                    'description': 'Выдавший орган',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
            },
            'Акт приемки в эксплуатацию законченного строительства': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'issuing_authority': {
                    'description': 'Выдавший орган',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
            },
            'Выписка из постановления': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'issuing_authority': {
                    'description': 'Выдавший орган',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
            },
            'Инвентаризационная карточка': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'issuing_authority': {
                    'description': 'Выдавший орган',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
            },
            'Извлечение из технического паспорта': {
                'number': {
                    'description': 'Номер',
                    'type': 'text',
                    'section': '',
                    'choices': []
                },
                'date': {
                    'description': 'Дата',
                    'type': 'date',
                    'section': '',
                    'choices': []
                },
                'issuing_authority': {
                    'description': 'Выдавший орган',
                    'type': 'choices',
                    'section': '',
                    'choices': []
                },
            },
            'Прочие типы документов': {}


        }

        for doc_type, attrs in doc_types_and_attrs.items():
            DocumentType.objects.get_or_create(name=doc_type, attributes=attrs)
