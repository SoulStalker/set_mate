from datetime import datetime, timedelta
from shifts import get_shifts, unclosed_shifts
from tg import TelegramBot
from config import token, chatid


def main():
    # Создаем экземпляры классов API
    shifts_api = get_shifts()
    telegram_api = TelegramBot(token=token, chat_id=chatid)

    sum_by_shop = {}
    for shift in shifts_api:
        shop_index = shift['shop_index']
        sum_by_checks = shift['sum_by_checks']
        if shop_index in sum_by_shop:
            sum_by_shop[shop_index] += sum_by_checks
        else:
            sum_by_shop[shop_index] = sum_by_checks

    for shop_index, revenue in sum_by_shop.items():
        print(f'Магазин № {shop_index}: {revenue:,.2f}'.replace(',', ' '))
        if shop_index in unclosed_shifts().keys():
            unclosed = unclosed_shifts()[shop_index]
            print(f'В Магазине не закрыта смена на кассе номер {" и ".join(map(str, unclosed))}')

    total = sum(sum_by_shop.values())
    if not unclosed_shifts():
        print(f'Во всех магазинах смены закрыты')
    print(f'Total sum: {total:,.2f}'.replace(',', ' '))

    # Проверяем наличие незакрытых смен
    # unclosed_shifts = shifts_api.check_unclosed_shifts(shifts)

    # Получаем данные о выручке и количестве чеков по магазинам
    # revenue_by_store = get_revenue_by_store(date_start, date_end)

    # Отправляем уведомление о незакрытых сменах, если такие имеются
    # if unclosed_shifts:
    #     telegram_api.send_message("Незакрытые смены:\n" + "\n".join(unclosed_shifts))
    #
    # # Отправляем уведомление о сменах с близкими номерами
    # close_shifts = shifts_api.check_close_shifts(shifts)
    # if close_shifts:
    #     telegram_api.send_message("Близкие номера смен:\n" + "\n".join(close_shifts))

    # Отправляем уведомление о выручке по магазинам
    message = "Выручка по магазинам за сегодня:\n"
    # for store, (revenue, checks_count) in revenue_by_store.items():
    #     message += f"{store}: {revenue} руб. ({checks_count} чеков)\n"
    # telegram_api.send_message(message)


if __name__ == "__main__":
    main()
