import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import giphy

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', '8443'))
TOKEN = os.environ.get('TOKEN')


# Определяем команды бота
def start(update, context):
    """Здесь отправляется приветственное сообщение"""
    text = "Привет! Этот бот выдает рандомные гифки с сайта https://giphy.com/, ровно одну за запрос."
    update.message.reply_text(text)


def help(update, context):
    """Типа справка"""
    update.message.reply_text('Пиши любой текст боту, он пришлет рандомный gif, что не понятно то!')


def echo(update, context):
    """Собственно работа бота - на любой текст отправлять гифку"""
    url = giphy.get_random_gif()
    update.message.reply_text('Рандомный gif. Надеюсь тебе повезло с ним :)')
    update.message.reply_animation(url)


def error(update, context):
    """Логируем ошибочки"""
    logger.warning(f"Обновление {update} вызвало ошибку {context.error}")


def main():
    """Запускаем бота"""
    try:
        updater = Updater(TOKEN, use_context=True)
    except ValueError:
        logger.error("Не предоставлен токен аутентификации. Запуск бота не возможен.")
        exit()

    dp = updater.dispatcher

    # определяем основные команды
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # обрабатываем любой ввод
    dp.add_handler(MessageHandler(Filters.text, echo))

    # пишем все ошибочки
    dp.add_error_handler(error)

    # Собственно начинаем проверять обновления на ТГ
    # updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.set_webhook("https://morning-taiga-79742.herokuapp.com/" + TOKEN)

    # Делаем бота убиваемым
    updater.idle()


if __name__ == '__main__':
    main()
