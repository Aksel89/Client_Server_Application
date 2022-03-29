"""
2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах. Написать
скрипт, автоматизирующий его заполнение данными. Для этого: Создать функцию write_order_to_json(), в которую передается
5 параметров — товар (item), количество (quantity), цена (price), покупатель (buyer), дата (date). Функция должна
предусматривать запись данных в виде словаря в файл orders.json. При записи данных указать величину отступа в 4
пробельных символа; Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений
каждого параметра.
"""
import json


def write_order_to_json(item, quantity, price, buyer, date):
    """
    The function writes data in the form of a dictionary to a json file
    :param item: item
    :param quantity: quantity
    :param price: price
    :param buyer: buyer
    :param date: date
    :return: result for write in json
    """

    with open('orders.json', 'r', encoding='utf-8') as f_r:
        data = json.load(f_r)

    with open('orders.json', 'w', encoding='utf-8') as f_w:
        orders_list = data['orders']
        order_info = {
            'item': item,
            'quantity': quantity,
            'price': price,
            'buyer': buyer,
            'date': date
        }
        orders_list.append(order_info)
        json.dump(data, f_w, indent=4, ensure_ascii=False)


write_order_to_json('шкаф', 5, 10800, 'Иванов А.А', '12.02.2022')
write_order_to_json('стул', 12, 3500, 'Петров Б.Б.', '13.02.2022')
