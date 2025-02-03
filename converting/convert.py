from datetime import datetime

import pandas as pd
import xml.etree.ElementTree as ET

from chudpo_bot.exceptions import ConversionError
from .constants import (CHUDPO, INPUT_FORMAT, OUTPUT_FORMAT,
                        TEST_COLUMNS, WORKER_COLUMNS)
from .validators import check_null_values


def converting_to_xml(xlsx_files, xml_file_path):
    # Создание корневого элемента XML
    registry_set = ET.Element(
        'RegistrySet',
        attrib={
            'xsi:noNamespaceSchemaLocation': 'schema.xsd',
            'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance'
        }
    )

    for file in xlsx_files:
        df = pd.read_excel(file)

        for index, row in df.iterrows():
            check_null_values(index, row)

            registry_record = ET.SubElement(registry_set, 'RegistryRecord')
            worker = ET.SubElement(registry_record, 'Worker')
            for col in WORKER_COLUMNS:
                ET.SubElement(worker, col).text = str(row[WORKER_COLUMNS[col]])

            organization = ET.SubElement(registry_record, 'Organization')
            for col in CHUDPO:
                ET.SubElement(organization, col).text = str(CHUDPO[col])

            test = ET.SubElement(registry_record,
                                 'Test',
                                 isPassed="true",
                                 learnProgramId=str(row[TEST_COLUMNS['id']]))

            try:
                date_str = row[TEST_COLUMNS['date']]
                # Преобразование даты в нужный формат
                date_object = datetime.strptime(date_str, INPUT_FORMAT)
                formatted_date = date_object.strftime(OUTPUT_FORMAT)
                ET.SubElement(test, 'Date').text = formatted_date
            except Exception as e:
                raise ConversionError(
                    f'Ошибка в строке {index + 2}, ячейка '
                    f'"{TEST_COLUMNS['date']}": {row[TEST_COLUMNS['date']]}.\n'
                    f'Причина: {str(e)}'
                )
            ET.SubElement(test, 'ProtocolNumber').text = str(
                row[TEST_COLUMNS['protocol']])
            ET.SubElement(
                test, 'LearnProgramTitle').text = row[TEST_COLUMNS['title']]

    with open(xml_file_path, 'wb') as f:
        # Запись декларации XML
        # (с двойными кавычками, иначе автоматически формируются одинарные)
        f.write(b'<?xml version="1.0" encoding="utf-8"?>\n')
        tree = ET.ElementTree(registry_set)
        # Установка xml_declaration=False
        tree.write(f, encoding='utf-8', xml_declaration=False)
