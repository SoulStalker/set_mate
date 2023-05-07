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
                Select os.shopindex, os.cashnum, os.numshift, os.operday, os.state, os.inn,
                        round(sum(op.checksumstart)/100, 2) as sub_total,
                        round(sum(op.checksumend)/100, 2) as total
                        from od_shift os 
                        join od_purchase op on os.id = op.id_shift 
                        where os.operday =%s and op.checkstatus = 0
                        group by os.cashnum, os.shopindex, os.numshift, os.operday, os.state, os.inn 
                        order by os.shopindex, os.cashnum 
                ''', (date.today(),))
    # получение результатов запроса
    rows = cur.fetchall()
    cur.close()
    conn.close()
    # преобразование результатов запроса в список словарей
    shifts_today = []
    for row in rows:
        shift = {'shop_index': row[0], 'cash_num': row[1], 'num_shift': row[2], 'operation_day': row[3],
                 'state': row[4], 'inn': row[5], 'sub_total': row[6], 'total': row[7]}
        shifts_today.append(shift)

    return shifts_today


if __name__ == '__main__':
    pprint(get_shifts())