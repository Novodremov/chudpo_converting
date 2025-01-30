import glob
import os
from datetime import datetime

from dotenv import load_dotenv
import pandas as pd
import xml.etree.ElementTree as ET

load_dotenv()

from constants import (CHUDPO, CONVERT_DIR, INPUT_FORMAT, OUTPUT_FORMAT,  # noqa
                       TEST_COLUMNS, WORKER_COLUMNS, XML_NAME_FORMAT)


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

input_folder = os.path.join(parent_dir, CONVERT_DIR, 'original_xlsx')
output_folder = os.path.join(parent_dir, CONVERT_DIR, 'converted_to_xml')


os.makedirs(output_folder, exist_ok=True)

# Получаем список всех файлов .xlsx в папке original_xlsx
xlsx_files = glob.glob(os.path.join(input_folder, '*.xlsx'))


def converting_to_xml(xlsx_files):
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

        # Добавление записей о работниках из текущего файла
        for index, row in df.iterrows():
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

            # Преобразование даты в нужный формат
            date_str = row[TEST_COLUMNS['date']]
            date_object = datetime.strptime(date_str, INPUT_FORMAT)
            formatted_date = date_object.strftime(OUTPUT_FORMAT)

            ET.SubElement(test, 'Date').text = formatted_date
            ET.SubElement(test, 'ProtocolNumber').text = str(
                row[TEST_COLUMNS['protocol']])
            ET.SubElement(
                test, 'LearnProgramTitle').text = row[TEST_COLUMNS['title']]

    output_file_name = f'{datetime.now().strftime(XML_NAME_FORMAT)}.xml'

    with open(os.path.join(output_folder, output_file_name), 'wb') as f:
        # Запись декларации XML
        # (с двойными кавычками, иначе автоматически формируются одинарные)
        f.write(b'<?xml version="1.0" encoding="utf-8"?>\n')
        tree = ET.ElementTree(registry_set)
        # Установка xml_declaration=False
        tree.write(f, encoding='utf-8', xml_declaration=False)

    print(f"XML файл сохранен: {os.path.join(
        output_folder, output_file_name)}")


converting_to_xml(xlsx_files)
