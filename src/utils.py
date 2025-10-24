import os

import pandas as pd
from pandas import DataFrame

ABSPATH_TO_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx")

def load_data(path: str = ABSPATH_TO_FILE) -> DataFrame:
    """Загружает данные из Excel-файла и возвращает объект DataFrame"""

    df = pd.read_excel(path)
    return df
