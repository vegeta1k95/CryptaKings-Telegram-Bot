import telebot
import config
from datetime import date
import random
import queue
import threading


class FastBot(telebot.TeleBot):

    def __init__(self, token):
        super().__init__(token=token)
        self.buffer = {}


    def check_buff(self, message):
        # Check if there is user_id in buffer
        _id = self.get_id(message)
        if self.buffer.get(_id, False) == False:
            self.buffer[_id] = dict()

    def get_id(self, message):
        # Extract ID from Message entity
        if type(message) == telebot.types.Message:
            return message.chat.id
        elif type(message) == telebot.types.CallbackQuery:
            return message.message.chat.id
        else:
            raise TypeError("Inncorect type of message.")

    def get_data(self, call):
        # Extract query info from callback data as dict
        try:
            string = call.data
            dct = dict(x.split("=") for x in string.split(","))
            return dct
        except Exception as e:
            pass

    def get_keyboard(self, input_array, grid=1):
        # Create Keyboard markup from the given input_array
        if type(input_array) == type(list()):
            for button in input_array:
                if type(button) != type(dict()):
                    raise TypeError("The input array must contain dictionaries.")
                elif button.get('text') == None or button.get('query') == None:
                    raise ValueError("The dictionary in the input array must contain the key 'text' and 'query'.")
        elif type(input_array) == type(dict()):
            if input_array.get('text') == None or input_array.get('query') == None:
                raise ValueError("The input array must contain the key 'text' and 'query'.")
        else:
            raise TypeError("The input array type must be list or dict.")
        if type(grid) == type(int()):
            if grid < 1 or grid > 7:
                raise ValueError("Incorrect number of columns in the grid.")
            else:
                amount = len(input_array)
                rows = amount // grid
                if rows == 0:
                    raise ValueError("Incorrect number of columns in the grid.")
                last_rows = amount % grid
                col = grid
                grid = list()
                for row in range(rows):
                    grid.append(col)
                if last_rows != 0:
                    grid.append(last_rows)
        elif type(grid) == type(list()):
            grid_amount = int()
            for row in grid:
                if type(row) == type(int()):
                    if row < 1 or row > 7:
                        raise ValueError("Incorrect number of columns in the grid.")
                    else:
                        grid_amount = grid_amount + row
                else:
                    raise TypeError("The value type in the grid must be int.")
            amount = len(input_array)
            if amount != grid_amount:
                raise ValueError("The sum of the columns in the grid must be equal to the length of the input array.")
        else:
            raise TypeError("The grid type must be int or list.")
        row_width = max(grid)
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=row_width)
        for col in grid:
            row = list()
            for i in range(col):
                button = input_array.pop(0)
                row.append(
                    telebot.types.InlineKeyboardButton(str(button.get('text')), switch_inline_query="",
                                                callback_data=str(button.get('query'))).to_dic())
            keyboard.keyboard.append(row)
        return keyboard

    def add_keyboard(self, keyboard, add):
        for row in add.keyboard:
            keyboard.keyboard.append(row)
        return keyboard

    def send_message(self, text, message, con="send", keyboard=None, parse_mode=None, disable_notification=None,
                     disable_web_page_preview=None):
        
        # Improved version of inherited send_message(...) method
        if type(keyboard) != telebot.types.InlineKeyboardMarkup and keyboard != None:
            raise TypeError("The keyboard type must be telebot.types.InlineKeyboardMarkup.")
        try:
            if type(message) == telebot.types.Message:
                if con == 'send':
                    try:
                        res = telebot.TeleBot.send_message(self, chat_id=message.chat.id, text=str(text), reply_markup=keyboard,
                                                 parse_mode=parse_mode, disable_notification=disable_notification,
                                                 disable_web_page_preview=disable_web_page_preview)
                        return res
                    except Exception as err:
                        res = telebot.TeleBot.send_message(self, chat_id=message.chat.id, text=str(text),
                                                     reply_markup=keyboard,
                                                     disable_notification=disable_notification,
                                                     disable_web_page_preview=disable_web_page_preview)
                        return res
                elif con == 'edit':
                    res = telebot.TeleBot.edit_message_text(self, text=str(text), chat_id=message.chat.id,
                                                      message_id=message.message_id, reply_markup=keyboard,
                                                      parse_mode=parse_mode,
                                                      disable_web_page_preview=disable_web_page_preview)
                else:
                    raise TypeError("Unknown message controller.")
            elif type(message) == telebot.types.CallbackQuery:
                if con == 'send':
                    try:
                        res = telebot.TeleBot.send_message(self, chat_id=message.message.chat.id, text=str(text),
                                                     reply_markup=keyboard, parse_mode=parse_mode,
                                                     disable_notification=disable_notification,
                                                     disable_web_page_preview=disable_web_page_preview)
                        return res
                    except Exception as err:
                        res = telebot.TeleBot.send_message(self, chat_id=message.message.chat.id, text=str(text),
                                                     reply_markup=keyboard,
                                                     disable_notification=disable_notification,
                                                     disable_web_page_preview=disable_web_page_preview)
                        return res
                elif con == 'edit':
                    res = telebot.TeleBot.edit_message_text(self, text=str(text), chat_id=message.message.chat.id,
                                                     message_id=message.message.message_id, reply_markup=keyboard,
                                                     parse_mode=parse_mode,
                                                     disable_web_page_preview=disable_web_page_preview)
                    return res
                else:
                    raise TypeError("Unknown message controller.")
            elif type(message) == type(str()):
                if con == 'send':
                    try:
                        res = telebot.TeleBot.send_message(self, chat_id=message, text=str(text), reply_markup=keyboard,
                                                 parse_mode=parse_mode, disable_notification=disable_notification,
                                                 disable_web_page_preview=disable_web_page_preview)
                        return res
                    except Exception as err:
                        res = telebot.TeleBot.send_message(self, chat_id=message, text=str(text),
                                                     reply_markup=keyboard,
                                                     disable_notification=disable_notification,
                                                     disable_web_page_preview=disable_web_page_preview)
                        return res
                elif con == 'edit':
                    res = telebot.TeleBot.edit_message_text(self, text=str(text), chat_id=message,
                                                      message_id=message.message_id, reply_markup=keyboard,
                                                      parse_mode=parse_mode,
                                                      disable_web_page_preview=disable_web_page_preview)
                else:
                    raise TypeError("Unknown message controller.")
            else:
                raise TypeError("The message type must be telebot.types.Message or telebot.types.CallbackQuery.")
        except Exception as err:
            print(repr(err))
