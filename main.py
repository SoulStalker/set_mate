from datetime import datetime, timedelta
from shifts import get_shifts, unclosed_shifts
from tg import TelegramBot
from config import token, chat_id, se


def main():
    # Создаем экземпляры классов API
    shifts_api = get_shifts()
    telegram_api = TelegramBot(token=token, chat_id=chat_id)

    sum_by_shop = {}
    for shift in shifts_api:
        shop_index = shift['shop_index']
        sum_by_checks = shift['sum_by_checks']
        if shop_index in sum_by_shop:
            sum_by_shop[shop_index] += sum_by_checks
        else:
            sum_by_shop[shop_index] = sum_by_checks

    for shop_index, revenue in sum_by_shop.items():
        print(f'Магазин {se[shop_index]} : {revenue:,.2f}'.replace(',', ' '))

        if shop_index in unclosed_shifts().keys():
            unclosed = unclosed_shifts()[shop_index]
            message = f'{se[shop_index]} \n не закрыта смена на кассе номер {" и ".join(map(str, unclosed))}'
            # telegram_api.send_message(message)
            print(message)

    total = sum(sum_by_shop.values())
    if not unclosed_shifts():
        telegram_api.send_message(f'Во всех магазинах смены закрыты')

    message = f'Выручка по магазинам за сегодня:\n {total:,.2f}'.replace(',', ' ')
    print(message)
    # for store, (revenue, checks_count) in revenue_by_store.items():
    #     message += f"{store}: {revenue} руб. ({checks_count} чеков)\n"
    # telegram_api.send_message(message)


if __name__ == "__main__":
    main()
