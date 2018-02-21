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
        # Проверка, есть ли юзер айди в переменной буффер бота
        _id = self.get_id(message)
        if self.buffer.get(_id, False) == False:
            # Если нет, то создать
            self.buffer[_id] = dict()

    def get_id(self, message):
        if type(message) == telebot.types.Message:
            return message.chat.id
        elif type(message) == telebot.types.CallbackQuery:
            return message.message.chat.id
        else:
            raise TypeError("Inncorect type of message.")

    def get_data(self, call):
        try:
            string = call.data
            dct = dict(x.split("=") for x in string.split(","))
            return dct
        except Exception as e:
            pass
            #self.send_message(call.message.chat.id, e)
    def get_keyboard(self, input_array, grid=1):
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

    def callendar(self, year, month):
        if int(month) < 1 or int(month) > 12 or type(month) != type(str()):
            raise ValueError("The value for the month should be within the range of 1 to 12 and have a string type")
        if int(year) < 0 or type(year) != type(str()):
            raise ValueError("The value for the year must be greater than zero and have a string type")
        callback_data = "m=" + month + ",y=" + year + ",c=call"
        callback_data_pre_y = "y=" + str(int(year) - 1) + ",m=" + month + ",c=call"
        callback_data_next_y = "y=" + str(int(year) + 1) + ",m=" + month + ",c=call"
        if int(month) > 1 and int(month) < 12:
            # Проверка ноходиться месяц на стыке нового или старого года
            callback_data_pre_m = "m=" + str(int(month) - 1) + ",y=" + year + ",c=call"
            callback_data_next_m = "m=" + str(int(month) + 1) + ",y=" + year + ",c=call"
            days = config.days[int(month) - 2]
        elif int(month) == 1:
            callback_data_pre_m = "m=" + str(12) + ",y=" + str(int(year) - 1) + ",c=call"
            callback_data_next_m = "m=" + str(int(month) + 1) + ",y=" + year + ",c=call"
            days = config.days[11]
        elif int(month) == 12:
            callback_data_pre_m = "m=" + str(int(month) - 1) + ",y=" + year + ",c=call"
            callback_data_next_m = "m=" + str(1) + ",y=" + str(int(year) + 1) + ",c=call"
            days = config.days[int(month) - 2]
        year_scroller = [{"text": chr(128281), "query": callback_data_pre_y}, {"text": year, "query": callback_data},
                         {"text": chr(128284), "query": callback_data_next_y}]
        month_scroller = [{"text": chr(128281), "query": callback_data_pre_m},
                          {"text": config.month[int(month) - 1], "query": callback_data},
                          {"text": chr(128284), "query": callback_data_next_m}]
        days_of_week = [{"text": "Пн", "query": callback_data}, {"text": "Вт", "query": callback_data},
                        {"text": "Ср", "query": callback_data}, {"text": "Чт", "query": callback_data},
                        {"text": "Пт", "query": callback_data}, {"text": "Сб", "query": callback_data},
                        {"text": "Вс", "query": callback_data}, ]
        f_day = date(int(year), int(month), 1).weekday()  # День недели первого дня месяца
        btn = 0  # Переменная для количества кнопок
        days_of_month = []
        add = 0  # Перемення для добавочного дня в высокостном году
        if abs(int(year) - 2016) % 4 == 0 and int(month) == 2:  # Проверка высокосного года
            add = 1
        for i in range(f_day):
            # Заполняем все дни прошлого месяца , если первое число текущего месяца приходит не на понеделник
            days_of_month.append(
                {"text": str(days - f_day + i + 1 + add),
                 "query": callback_data_pre_m + ",d=" + str(i + 1) + ',c=soon,con=edit'})
            btn += 1
        ts = ["🗨", "👁‍🗨", "💬"]
        for i in range(config.days[int(month) - 1] + add):  # Клавиатура дней
            if int(date.today().strftime("%Y")) == int(year) and int(date.today().strftime("%m")) == int(month) and int(
                    date.today().strftime(
                        "%d")) == int(str(i + 1)):
                days_of_month.append({"text": chr(128205),
                                      "query": callback_data + ",d=" + str(i + 1) + ',c=soon,con=edit'})
            else:
                add = random.choice(ts)
                days_of_month.append({"text": str(i + 1) + "|" + str(random.randint(1, 10)),
                                      "query": callback_data + ",d=" + str(i + 1) + ',c=soon,con=edit'})
            btn += 1
        if btn % 7 != 0:
            for i in range(7 - btn % 7):
                days_of_month.append({"text": str(i + 1),
                                      "query": callback_data_next_m + ",d=" + str(i + 1) + ',c=soon,con=edit'})
        keyboard = year_scroller + month_scroller + days_of_week + days_of_month
        grid = [3, 3, 7]
        for i in range(int(len(days_of_month) / 7)):
            grid.append(7)
        keyboard = self.get_keyboard(input_array=keyboard, grid=grid)
        return keyboard

    def scroller(self, page_num, count, query_str, btn_num=5, curr_str=None, pre_str=None,
                       next_str=None, query_page='pg', ):
        mrkp = []
        if page_num < (btn_num // 2 + 1):
            if (page_num + btn_num - 1) >= count and count <= 7:
                print('4')
                for i in range(1, count + 1):
                    if i == page_num:
                        if curr_str == None:
                            curr_str = "• " + str(int(i)) + " •"
                        mrkp.append({"text": curr_str, "query": query_str + ',' + query_page + '=' + str(int(i))})
                    else:
                        mrkp.append({"text": str(int(i)), "query": query_str + ',' + query_page + '=' + str(int(i))})
            else:
                print('3')
                for i in range(1, btn_num):
                    if i == page_num:
                        if curr_str == None:
                            curr_str = "• " + str(int(i)) + " •"
                        mrkp.append({"text": curr_str, "query": query_str + ',' + query_page + '=' + str(int(i))})
                    else:
                        mrkp.append({"text": str(int(i)), "query": query_str + ',' + query_page + '=' + str(int(i))})
                if next_str == None:
                    next_str = str(int(btn_num))
                mrkp.append({"text": next_str, "query": query_str + ',' + query_page + '=' + str(int(btn_num))})
        elif page_num >= (btn_num // 2 + 1) and page_num < (count - btn_num // 2):
            print('5')
            if pre_str == None:
                pre_str = str(int(page_num - btn_num // 2))
            mrkp.append({"text": pre_str, "query": query_str + ',' + query_page + '=' + str(int(page_num - btn_num // 2))})
            for i in range((page_num - btn_num // 2 + 1), (page_num + btn_num // 2)):
                if i == page_num:
                    if curr_str == None:
                        curr_str = "• " + str(int(i)) + " •"
                    mrkp.append({"text": curr_str, "query": query_str + ',' + query_page + '=' + str(int(i))})
                else:
                    mrkp.append({"text": str(int(i)), "query": query_str + ',' + query_page + '=' + str(int(i))})
            if next_str == None:
                next_str = str(int(page_num + btn_num // 2))
            mrkp.append(
                {"text": next_str, "query": query_str + ',' + query_page + '=' + str(int(page_num + btn_num // 2))})
        elif page_num >= (count - btn_num // 2):
            if btn_num < count:
                print('1')
                if pre_str == None:
                    pre_str = str(int(count - btn_num))
                mrkp.append({"text": pre_str, "query": query_str + ',' + query_page + '=' + str(int(count - btn_num))})
                for i in range((count - btn_num + 1), count):
                    if i == page_num:
                        if curr_str == None:
                            curr_str = "• " + str(int(i)) + " •"
                        mrkp.append({"text": curr_str, "query": query_str + ',' + query_page + '=' + str(int(i))})
                    else:
                        mrkp.append({"text": str(int(i)), "query": query_str + ',' + query_page + '=' + str(int(i))})
            elif btn_num >= count:
                print('2')
                for i in range(1, count + 1):
                    if i == page_num:
                        if curr_str == None:
                            curr_str = "• " + str(int(i)) + " •"
                        mrkp.append({"text": curr_str, "query": query_str + ',' + query_page + '=' + str(int(i))})
                    else:
                        mrkp.append({"text": str(int(i)), "query": query_str + ',' + query_page + '=' + str(int(i))})

        return self.get_keyboard(input_array=mrkp, grid=min(count, btn_num))
