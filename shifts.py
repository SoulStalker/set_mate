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
    cur.execute('''
                SELECT os.shopindex, os.cashnum, os.numshift, os.operday, os.state, os.inn,
                      count(case when op.cash_operation = 0 then op.checksumstart else null end) as check_count,
                      sum(case when op.cash_operation = 0 then op.checksumend else -op.checksumend end)/100 as sum_by_checks
                            FROM od_shift os
                            JOIN od_purchase op ON os.id = op.id_shift
                            WHERE os.operday = %s and op.checkstatus = 0
                            GROUP BY os.cashnum, os.shopindex, os.numshift, os.operday, os.state, os.inn
                            ORDER BY os.shopindex, os.cashnum
                ''', (date.today(),))
    # получение результатов запроса
    rows = cur.fetchall()
    cur.close()
    conn.close()
    # преобразование результатов запроса в список словарей
    shifts_today = []
    for row in rows:
        shift = {'shop_index': row[0], 'cash_num': row[1], 'num_shift': row[2], 'operation_day': row[3],
                 'state': row[4], 'inn': row[5], 'checks_count': row[6], 'sum_by_checks': row[7]}
        shifts_today.append(shift)

    return shifts_today


def unclosed_shifts():
    unclosed = {}
    for shift in get_shifts():
        if not shift['state']:
            unclosed.setdefault(shift['shop_index'], set()).add(shift['cash_num'])

    return unclosed


if __name__ == '__main__':
    pprint(get_shifts())
    print(unclosed_shifts())