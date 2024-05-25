import datetime
import os
import pathlib

PATH_TO_CHECK = f"{pathlib.Path(__file__).parent.absolute()}/test_folder/"


def check_and_delete(path_to_check: str, amount_days: int, mode: str) -> None:
    """
    Функция удаления файлов старше N-дней.
    Для проверки по дате создания файла - передать в параметр mode значение "created".
    Для проверки по дате изменения файла - передать в параметр mode значение "modified"
    """
    # дата сегодня
    today = datetime.date.today()
    # цикл по файлам по переданному пути каталога
    for root, dirs, files in os.walk(path_to_check):
        for file in files:
            full_path = os.path.join(root, file)
            # условие, какой атрибут времени проверяем
            # в зависимости от режима
            if mode == "created":
                time_attribute = datetime.date.fromtimestamp(
                    os.path.getctime(full_path)
                )
            if mode == "modified":
                time_attribute = datetime.date.fromtimestamp(
                    os.path.getmtime(full_path)
                )
            # разность времен текущего и файла
            diff_times = today - time_attribute
            # переводим разность в количество дней
            days_count = int(diff_times.days)
            # проверяем превышение количества дней
            # и удаляем, если верно
            if days_count > amount_days:
                os.remove(full_path)


if __name__ == "__main__":
    check_and_delete(PATH_TO_CHECK, 10, "created")
