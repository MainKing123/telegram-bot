import telebot
from config import TOKEN
from extensions import CurrencyConverter, APIException

bot = telebot.TeleBot(TOKEN)
currencies = {
    'USD': 'Доллар США',
    'EUR': 'Евро',
    'RUB': 'Российский рубль'
}

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    instructions = """
Чтобы узнать цену валюты, отправьте сообщение в формате:
<имя валюты> <имя валюты для перевода> <количество>
Например: USD EUR 100

Доступные команды:
/values - список доступных валют
/help - помощь по использованию бота
"""
    bot.reply_to(message, instructions)

@bot.message_handler(commands=['values'])
def handle_values(message):
    text = "Доступные валюты:\n"
    for key, value in currencies.items():
        text += f"{key} - {value}\n"
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def handle_convert(message):
    try:
        values = message.text.upper().split()
        
        if len(values) != 3:
            raise APIException("Неверное количество параметров")

        base, quote, amount = values

        if base not in currencies:
            raise APIException(f"Валюта {base} не найдена")
        if quote not in currencies:
            raise APIException(f"Валюта {quote} не найдена")

        result = CurrencyConverter.get_price(base, quote, amount)
        text = f"{amount} {base} = {result:.2f} {quote}"
        bot.reply_to(message, text)
        
    except APIException as e:
        bot.reply_to(message, f"Ошибка ввода: {str(e)}")
    except Exception as e:
        bot.reply_to(message, f"Системная ошибка: {str(e)}")

bot.polling(none_stop=True)
