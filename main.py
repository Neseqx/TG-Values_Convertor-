import telebot
from config import keys, TOKEN
from extensions import ValuesConverter, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_tutorial(message):
    bot.send_message(message.chat.id, 'Для работы бота введите данные в следующем формате: \n '
                                      '<Название валюты> => <Название валюты, в которую надо перевести> => '
                                      '<Количество валюты>')


@bot.message_handler(commands=['values'])
def value(message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def get_price(message):
    try:
        values = message.text.split(' ')
        quote, base, amount = values
        total_base = ValuesConverter.converter(quote, base, amount)

        if len(values) != 3:
            raise APIException('На ввод принимаются 3 параметра: \nПример: \nВвод пользователя: <доллар> <рубль> <1> '
                               '\nОтвет: 93.78')

    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка ввода пользователя \n{e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Не удалось обработать команду \n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()