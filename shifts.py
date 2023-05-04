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

    # выполнение запроса к базе данных
    cur.execute("SELECT * FROM od_shift")

    # получение результатов запроса
    rows = cur.fetchall()

    # закрытие соединения с базой данных
    cur.close()
    conn.close()

    return rows


if __name__ == '__main__':
    print(get_shifts())