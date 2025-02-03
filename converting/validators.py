from chudpo_bot.exceptions import ConversionError


def check_null_values(index, row):
    if row.isnull().any():
        raise ConversionError(
            f'Ошибка в строке {index + 2}: найдены пустые значения.'
        )
