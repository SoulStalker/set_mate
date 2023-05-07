from datetime import datetime, timedelta
from shifts import get_shifts
from tg import TelegramBot
from config import token, chatid


def main():
    # Создаем экземпляры классов API
    shifts_api = get_shifts()
    telegram_api = TelegramBot(token=token, chat_id=chatid)
    # db_api = get_shifts_info()
    # Получаем данные о сменах
    sum_by_shop = {}
    for shift in shifts_api:
        shop_index = shift['shop_index']
        sub_total = shift['sub_total']
        if shop_index in sum_by_shop:
            sum_by_shop[shop_index] += sub_total
        else:
            sum_by_shop[shop_index] = sub_total
    for shop_index, fiscal_sum in sum_by_shop.items():
        print(f'{shop_index}: {fiscal_sum}')
    total = sum(sum_by_shop.values())
    print(f'Total sum: {total}')
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
