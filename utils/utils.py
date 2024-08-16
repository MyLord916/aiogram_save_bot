from datetime import datetime

subsequence = 1  # Последнее значение в нейминге файлов для уникальности имени


def get_dt_name() -> str:
    """Функция задает имя файла в формате времени год/месяц/день/минуты/(последовательный номер уникальности)"""
    global subsequence
    dt = datetime.now()
    dt_name = dt.strftime('%Y%m%d%H%M') + f'({str(subsequence)})' + '.jpg'
    if subsequence < 99:
        subsequence += 1
    else:
        subsequence = 1
    return dt_name


def set_correct_path(path) -> str:
    return '/'.join(path) + '/'
