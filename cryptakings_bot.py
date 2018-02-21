import fasttelegramapi as ft
import config

from functions import *

if __name__ == '__main__':
    
    bot = ft.FastBot(config.BOT_TOKEN)

    @bot.message_handler(commands=['start'])
    def start(message):
        start_menu(bot=bot, message=message)

    @bot.message_handler(commands=['menu'])
    def menu(message):
        main_menu(bot=bot, message=message)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_ans(call):
        get_callback(bot=bot, call=call)

    @bot.message_handler(content_types=["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice"])
    def post_ans(message):
        get_message(bot=bot, message=message)
    
    bot.polling(none_stop=True)
