import emoji as emj
import models

models.create_tables()

def user_reg(user_id):
    user = models.get_user_tg(user_id)
    if not user:
        user = models.new_user(user_id)

def check_user_log(user_id):
    user = models.get_user_tg(user_id)
    if user.logged_in:
        return True
    return False

def check_credentials(login, pwd, user_id):
    user = models.get_user_tg(user_id)
    if user.login(login, pwd):
        return True
    return False

def start_menu(bot, message):
    user_reg(message.chat.id)
    if check_user_log(message.chat.id):
        main_menu(bot, message)
    else:
        login_ask(bot, message, controller='send')

def login_ask(bot, message, controller='send'):
    _id = bot.get_id(message)
    text = """Welcome to CryptaKings Bot!
You have no CryptaKings account connected at the moment.
Would you like to connect to it?"""
    bot.buffer[_id] = {}
    input_keyboard = [{'text': emj.yes + ' Yes', 'query': 'c=login'},
                      {'text': emj.no + ' No', 'query': 'c=main_menu'}]

    keyboard = bot.get_keyboard(input_array=input_keyboard, grid=2)
    bot.send_message(text=text, message=message,
                     con=controller, keyboard=keyboard)

def logout(bot, message):
    _id = bot.get_id(message)
    user = models.get_user_tg(_id)
    user.logout()
    
    bot.send_message(text='You have been logged out!', message=message,
                     con='edit')
    main_menu(bot, message, controller="send")

def show_trades(bot, message):
    _id = bot.get_id(message)
    user = models.get_user_tg(_id)
    trades = user.get_transactions()

    text = """Your recent trades:"""

    input_keyboard = [{"text": emj.no + " Back to menu", "query": "c=main_menu"}]
    keyboard = bot.get_keyboard(input_array=input_keyboard, grid=1)
    bot.send_message(text=text, message=message, con='edit',
                     keyboard=keyboard)    

def request_login(bot, message):
    _id = bot.get_id(message)
    bot.buffer[_id] = {'wait': 'login'}
    text = "Please enter login to your CryptaKings account:"
    bot.send_message(text=text, message=message, con='send')

def request_password(bot, message):
    _id = bot.get_id(message)
    text = "Please enter password to your CryptaKings account:"
    bot.send_message(text=text, message=message, con='send')

def main_menu(bot, message, controller="send"):
    _id = bot.get_id(message)
    bot.buffer[_id] = {}
    text = """Welcome to CryptaKings Bot!
                 Main menu:"""

    input_keyboard = []
    user = models.get_user_tg(_id)
    
    if user.logged_in:
        if user.first_name and user.last_name:
            text = """Welcome to CryptaKings Bot, {0} {1}!
                 Main menu:""".format(user.first_name, user.last_name)
        input_keyboard.append({"text": emj.head + " My profile", "query": "c=profile"})
        input_keyboard.append({"text": emj.card + " My trades", "query": "c=trades"})
        
    else:
        input_keyboard.append({"text": emj.wrench + " Login", "query": "c=login"})

    #input_keyboard.append({"text": emj.news + " Latest news", "query": "c=news"})
    input_keyboard.append({"text": emj.plot + " Rankings", "query": "c=rankings"})

    if user.logged_in:
        input_keyboard.append({"text": emj.door + " Logout", "query": "c=logout"})

    keyboard = bot.get_keyboard(input_array=input_keyboard, grid=1)

    #with open('logo_notransparent.png', 'rb') as logo:
    logo = 'AgADAgADsqgxG2emsUhTGwQ2PbMxJXD1mw4ABPHmKSJ2c2ixxOQBAAEC'
    if controller == 'send':
        bot.send_photo(chat_id=message.chat.id, photo=logo)
    bot.send_message(text=text, message=message, con=controller,
                         keyboard=keyboard)
    
    
def get_callback(bot, call):
    _id = bot.get_id(call)
    bot.check_buff(call)
    dct = bot.get_data(call)

    command = dct.get('c')
    
    if command == 'main_menu':
        main_menu(bot, call.message, controller="edit")
        
    elif command == 'login':
        request_login(bot, call.message)

    elif command == 'logout':
        logout(bot, call.message)
        
    elif command == 'profile':
        pass
    elif command == 'trades':
        show_trades(bot, call.message)
        
    elif command == 'news':
        pass
    elif command == 'rankings':
        pass
    
def get_message(bot, message):
    _id = bot.get_id(message)
    bot.check_buff(message)
    dct = bot.buffer[_id]
    wait = dct.get('wait', None)

    if wait == 'login':
        bot.buffer[_id].update(wait='password', login=message.text)
        request_password(bot, message)
        
    elif wait == 'password':
        _login = bot.buffer[_id]['login']
        _password = message.text

        if check_credentials(_login, _password, _id):
            bot.send_message(text="Account has been succesfully connected!", message=message)
            main_menu(bot, message, controller='send')
        else:
            bot.send_message(text="Oops! Wrong login or password. Please try again.", message=message)
            main_menu(bot, message, controller='send')

def send_notification(data, bot=None):
    print(bot)
    print(data)
