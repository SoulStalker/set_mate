from datetime import datetime, timedelta
from shifts import get_shifts, unclosed_shifts, near_shifts
from tg import TelegramBot
from config import token, chat_id, se, legals


def main():
    # Создаем экземпляры классов API
    shifts_api = get_shifts()
    telegram_api = TelegramBot(token=token, chat_id=chat_id)

    sum_by_shop = {}
    for shift in shifts_api:
        shop_index = shift['shop_index']
        sum_by_checks = shift['sum_by_checks']
        checks_count = shift['checks_count']
        if shop_index in sum_by_shop:
            sum_by_shop[shop_index]['sum_by_checks'] += sum_by_checks
            sum_by_shop[shop_index]['sum_by_checks'] += checks_count
        else:
            sum_by_shop[shop_index] = {'sum_by_checks': sum_by_checks, 'checks_count': checks_count}

    for shop_index, revenue in sum_by_shop.items():
        message = f'Отчет за сегодня {se[shop_index]}:\n' \
                  f'Чеки: {revenue["checks_count"]}\n' \
                  f'Оборот: {revenue["sum_by_checks"]:,.2f} '.replace(',', ' ')
        print(message)
        # telegram_api.send_message(message)

        if shop_index in unclosed_shifts().keys():
            unclosed = unclosed_shifts()[shop_index]
            message = f'{se[shop_index]} \n не закрыта смена на кассе номер {" и ".join(map(str, unclosed))}'
            # telegram_api.send_message(message)
            print(message)

    total_sum = 0
    total_count = 0

    for shop, values in sum_by_shop.items():
        total_sum += values['sum_by_checks']
        total_count += values['checks_count']

    # if not unclosed_shifts():
        # telegram_api.send_message(f'Во всех магазинах смены закрыты')

    message = f'Суммарный отчет за сегодня:\n' \
              f'Чеки: {round(total_count)}\n' \
              f'Оборот: {total_sum:,.2f}'.replace(',', ' ')
    print(message)
    # telegram_api.send_message(message)

    for shop_cash, this_shift in near_shifts(get_shifts()).items():
        shop, cash = shop_cash
        shifts = this_shift
        nears = ()
        for shift in shifts:
            for k, v in shift.items():
                m = f'Смена {k} на фирме {legals[v]}'
            nears += (m,)
        message = f'{se[shop]}, касса номер {cash} близкие номера смен:\n' \
                  f'{" и ".join(nears)}\nрекомендуется переоткрыть смены на основной фирме'
        # telegram_api.send_message(message)
        print(message)


if __name__ == "__main__":
    main()
