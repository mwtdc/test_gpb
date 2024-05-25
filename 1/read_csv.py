import pathlib

import pandas as pd

ABSOLUTE_PATH = pathlib.Path(__file__).parent.absolute()
FILENAME = f"{ABSOLUTE_PATH}/csv_data.csv"
CSV_DATAFRAME = pd.read_csv(FILENAME, delimiter="|")


def get_unique_records(csv_dataframe: pd.DataFrame) -> None:
    """
    Функция сбора уникальных записей.
    """
    # Сбор уникальных записей
    unique_records = csv_dataframe.drop_duplicates(
        subset=["lastname", "name", "patronymic", "date_of_birth", "id"],
        keep="last",
    )
    # Сохранение уникальных записей в новый файл
    unique_records.to_csv(f"{ABSOLUTE_PATH}/unique_records.csv", index=False, sep="|")


def get_conflicting_records(csv_dataframe: pd.DataFrame) -> None:
    """
    Функция сбора конфликтных по id записей.
    """
    # Группировка по 'id' для дальнейшего поиска
    grouped_dataframe = csv_dataframe.groupby("id")
    # Поиск групп с более чем одним уникальным набором данных
    conflicting_records = pd.DataFrame()
    for id, group in grouped_dataframe:
        if len(group.drop_duplicates()) > 1:
            conflicting_records = pd.concat([conflicting_records, group])
    # Сохранение конфликтных записей в отдельный файл
    conflicting_records.to_csv(
        f"{ABSOLUTE_PATH}/conflicting_records.csv", index=False, sep="|"
    )


if __name__ == "__main__":
    get_unique_records(CSV_DATAFRAME)
    get_conflicting_records(CSV_DATAFRAME)
