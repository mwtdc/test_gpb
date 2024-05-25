import datetime
import logging
import pathlib
from sys import platform
from typing import Dict, Union

import pandas as pd
import requests
from pydantic import BaseModel, ValidationError
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def configure_logger() -> None:
    """
    Функция конфигурирования файла лога.
    """
    log_format = "%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s"
    if platform == "linux" or platform == "linux2":
        log_file = ("/var/log/log-execute/api_gazprombank_log.txt",)
    elif platform == "win32":
        log_file = (
            f"{pathlib.Path(__file__).parent.absolute()}/api_gazprombank_log.txt",
        )

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format=log_format,
    )


# Инициализация логера
configure_logger()

# начало дня сегодня в виде таймстемп
TIMESTAMP_START_DAY = int(
    datetime.datetime.today()
    .replace(hour=0, minute=0, second=0, microsecond=0)
    .timestamp()
)


class Document(BaseModel):
    """
    Модель данных для валидации JSON.
    """

    key1: int
    key2: datetime.datetime
    key3: str


def get_json(url: str, params: Dict) -> Union[Dict, None]:
    """
    Функция получения JSON GET-запросом на эндпоинт.
    """
    retry_strategy = Retry(
        total=3,
        status_forcelist=[101, 429, 500, 502, 503, 504],
        method_whitelist=["GET", "POST"],
        backoff_factor=1,
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    try:
        url_response = session.get(url, params, verify=False)
        if url_response.ok:
            json_string = url_response.json()
            logging.info("JSON из внешнего API получен.")
            return json_string

    except Exception as err:
        print(f"Ошибка получения JSON: {err}")
        logging.error(f"Ошибка получения JSON: {err}")


def validate_json(json_string: Dict) -> Union[Document, None]:
    """
    Функция валидации JSON.
    """
    try:
        Document.model_validate(json_string)
    except ValidationError as e:
        logging.error(f"Ошибка валидации JSON: {e}")
        print(e)


def dataframe_transformation(json_string: Dict) -> pd.DataFrame:
    """
    Функция преобразования полученного JSON в датафрейм.
    """
    dataframe = pd.DataFrame(
        data=json_string["Rows"],
        columns=json_string["Columns"],
    )
    dataframe.rename(
        columns={
            "key1": "document_id",
            "key2": "document_dt",
            "key3": "document_name",
        },
        errors="raise",
        inplace=True,
    )
    dataframe["load_dt"] = datetime.datetime.now().isoformat()
    return dataframe


def main() -> Union[pd.DataFrame, None]:
    """
    Основная функция.
    """
    params = {"documents_date": TIMESTAMP_START_DAY}
    url = "https://api.gazprombank.ru/very/important/docs"

    json_string = get_json(url, params)
    if json_string:
        valid_json = validate_json(json_string)
        if valid_json:
            dataframe = dataframe_transformation(valid_json)
            return dataframe


if __name__ == "__main__":
    dataframe = main()
    if dataframe:
        print(dataframe)
    else:
        print("Не удалось получить и обработать данные.")
