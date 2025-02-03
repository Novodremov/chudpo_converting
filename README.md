# Бот для ЧУДПО «Центр профессионального обучения г. Дзержинска»

## Описание

Бот умеет принимать файлы формата xlsx и преобразовывать их в формат xml по установленным настройкам.

## Технологии
```
- Python 3.12
- pyTelegramBotAPI
- pandas
- openpyxl
- python-dotenv
```

## Установка

### Порядок действий для запуска проекта

Клонировать репозиторий:
```bash
git clone git@github.com:Novodremov/chudpo_converting.git
```

Перейти в папку с проектом:
```bash
cd chudpo_converting
```

Создать и активировать виртуальное окружение:
```bash
python -m venv venv
```

* Для Linux/MacOS
    ```bash
    source venv/bin/activate
    ```

* Для Windows
    ```bash
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:
```bash
pip install -r requirements.txt
```

В корне проекта создать файл .env, заполнить его по аналогии с имеющимся в репозитории файлом .env.example.

Запустить проект:
```bash
python main.py
```

С помощью библиотеки pyinstaller можно скомпилировать exe-файл для работы бота. Процесс будет сворачиваться в трей. В корневую директорию проекта необходимо выложить файл иконки logo.png (эта иконка будет отображаться в трее). Файл main.exe компилируется в директории /dist по команде:
```
pyinstaller --onefile --windowed --icon=logo.png --add-data "logo.png;." --add-data ".env;." main.py
```


## Автор
*Лысов Алексей*
Контактная информация: 
- Электронная почта: [alexei.lysov@gmail.com](mailto:alexei.lysov@gmail.com)
- Telegram: [@nvdrmv](https://t.me/nvdrmv)
