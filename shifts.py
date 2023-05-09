import psycopg2

from config import report_day, dsn


def get_shifts():
    """
    Функция получает данные о сменах из базы данных.
    :return: list of dicts
    """
    conn = psycopg2.connect(**dsn)
    cur = conn.cursor()
    cur.execute('''
                SELECT os.shopindex, os.cashnum, os.numshift, os.operday, os.state, os.inn,
                      count(case when op.cash_operation = 0 then op.checksumstart else null end) as check_count,
                      sum(case when op.operationtype then op.checksumend else -op.checksumend end)/100 as sum_by_checks
                            FROM od_shift os
                            JOIN od_purchase op ON os.id = op.id_shift
                            WHERE os.operday = %s and op.checkstatus = 0
                            GROUP BY os.cashnum, os.shopindex, os.numshift, os.operday, os.state, os.inn
                            ORDER BY os.shopindex, os.cashnum
                ''', (report_day,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    shifts_today = []
    for row in rows:
        shift = {'shop_index': row[0], 'cash_num': row[1], 'num_shift': row[2], 'operation_day': row[3],
                 'state': row[4], 'inn': row[5], 'checks_count': row[6], 'sum_by_checks': row[7]}
        shifts_today.append(shift)

    return shifts_today


def unclosed_shifts():
    """
    Функция возвращает список незакрытых смен.
    :return: dict
    """
    unclosed = {}
    for shift in get_shifts():
        if not shift['state']:
            unclosed.setdefault(shift['shop_index'], set()).add(shift['cash_num'])

    return unclosed


def near_shifts(shift_rows):
    """
    Функция принимает список смен и возвращает словарь со сменами,
    у которых номера в разрезе кассы близки друг к другу.
    :param shift_rows: список смен
    :return: dict
    """
    near_shifts_list = []
    for i in range(len(shift_rows)):
        for j in range(i + 1, len(shift_rows)):
            if (shift_rows[i]['shop_index'] == shift_rows[j]['shop_index'] and
                    shift_rows[i]['cash_num'] == shift_rows[j]['cash_num'] and
                    abs(shift_rows[i]['num_shift'] - shift_rows[j]['num_shift']) <= 5):
                near_shifts_list.append(shift_rows[i])
                near_shifts_list.append(shift_rows[j])
    cleared_dict = {}
    for near in near_shifts_list:
        cleared_dict.setdefault((near['shop_index'], near['cash_num']), []).append({near['num_shift']: near['inn']})

    return cleared_dict


if __name__ == '__main__':
    """
    Проверочный вывод.
    """
    print(get_shifts())
    print(near_shifts(get_shifts()))
