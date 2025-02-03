import os

# Данные обучаемого работника
WORKER_COLUMNS = {'LastName': 'Фамилия',
                  'FirstName': 'Имя',
                  'MiddleName': 'Отчество',
                  'Snils': 'СНИЛС',
                  'Position': 'Должность',
                  'EmployerInn': 'ИНН организации-клиента',
                  'EmployerTitle': 'Наименование организации-клиента'
                  }

# Данные обучающей организации
CHUDPO = {'Inn': os.getenv('CHUDPO_INN'),
          'Title': os.getenv('CHUDPO_TITLE')
          }

# Информация по обучению
TEST_COLUMNS = {'date': 'Дата в удостоверении',
                'protocol': 'Номер протокола',
                'title': 'Наименование программы в Гос. Реестре',
                'id': 'ID программы в Гос. Реестре'
                }

REQUIRED_COLUMNS = set(WORKER_COLUMNS.values()
                       ).union(set(TEST_COLUMNS.values()))

INPUT_FORMAT = '%d.%m.%Y'
OUTPUT_FORMAT = '%Y-%m-%d'
XML_NAME_FORMAT = '%Y-%m-%d_%H-%M-%S'

CONVERT_DIR = 'converting'
