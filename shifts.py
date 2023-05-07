from datetime import datetime, date
from pprint import pprint

import psycopg2


def get_shifts():
    # установка соединения с базой данных
    conn = psycopg2.connect(
        host="192.168.10.231",
        database="set_operday",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    # получение даты начала и конца дня
    today_start = datetime.combine(date.today(), datetime.min.time())
    today_end = datetime.combine(date.today(), datetime.max.time())
    # выполнение запроса к базе данных
    cur.execute("SELECT * FROM od_shift WHERE shiftopen >= %s AND shiftopen <= %s", (today_start, today_end))
    # получение результатов запроса
    rows = cur.fetchall()
    cur.close()
    conn.close()
    # преобразование результатов запроса в список словарей
    shifts_today = []
    for row in rows:
        shift = {'id': row[0], 'cash_num': row[1], 'num_shift': row[5], 'shift_create': row[7],
                 'shift_close': row[8], 'shift_open': row[9], 'shop_index': row[10], 'state': row[11],
                 'operation_day': row[13]}
        shifts_today.append(shift)

    return shifts_today


if __name__ == '__main__':
    pprint(get_shifts())
