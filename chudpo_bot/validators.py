from io import BytesIO
import pandas as pd

from converting.constants import REQUIRED_COLUMNS


def check_necessary_columns(file):
    df = pd.read_excel(BytesIO(file))
    return REQUIRED_COLUMNS - set(df.columns)
