import emoji as emj

def user_reg(user_id):    
    return True

def check_user_log(user_id):
    return False

def check_credentials(login, pwd, user_id):
    return True

def get_post_data(message):
    text = None
    file_id = None
    if message.content_type == "text":
        text = message.text
    elif message.content_type == "photo":
        file_id = message.photo[-1].file_id
        text = message.caption
    elif message.content_type == "video":
        file_id = message.video.file_id
        text = message.caption
    elif message.content_type == "video_note":
        file_id = message.video_note.file_id
    elif message.content_type == "audio":
        file_id = message.audio.file_id
        text = message.caption
    elif message.content_type == "voice":
        file_id = message.voice.file_id
    elif message.content_type == "sticker":
        file_id = message.sticker.file_id
    elif message.content_type == "document":
        file_id = message.document.file_id
        text = message.caption
    post_type = message.content_type
    return text, file_id, post_type

def start_menu(bot, message):
    user_reg(message.chat.id)
    if check_user_log(message.chat.id):
        main_menu(bot, message, logged_in=True)
    else:
        login_ask(bot, message, controller='send')

def login_ask(bot, message, controller='send'):
    _id = bot.get_id(message)
    text = """Welcome to CryptaKings Bot!
You have no CryptaKings account connected at the moment.
Would you like to connect to it?"""
    bot.buffer[_id] = {}
    input_keyboard = [{'text': emj.yes + ' Yes', 'query': 'c=login'},
                      {'text': emj.no + ' No', 'query': 'c=main_menu,log=False'}]

    keyboard = bot.get_keyboard(input_array=input_keyboard, grid=2)
    bot.send_message(text=text, message=message,
                     con=controller, keyboard=keyboard)

def logout(bot, message):
    # user logout
    bot.send_message(text='You have been logged out!', message=message,
                     con='edit')
    main_menu(bot, message, controller="send", logged_in=False)

def request_login(bot, message):
    _id = bot.get_id(message)
    bot.buffer[_id] = {'wait': 'login'}
    text = "Please enter login to your CryptaKings accout:"
    bot.send_message(text=text, message=message, con='send')

def request_password(bot, message):
    _id = bot.get_id(message)
    text = "Please enter password to your CryptaKings accout:"
    bot.send_message(text=text, message=message, con='send')

def main_menu(bot, message, controller="send", logged_in=True):
    _id = bot.get_id(message)
    bot.buffer[_id] = {}
    text = """Welcome to CryptaKings Bot!
                 Main menu:"""

    input_keyboard = []

    if logged_in:
        input_keyboard.append({"text": emj.head + " My profile", "query": "c=profile"})
        input_keyboard.append({"text": emj.card + " My trades", "query": "c=trades"})
        
    # TODO Admin Rights/Functionality
    else:
        input_keyboard.append({"text": emj.wrench + " Login", "query": "c=login"})

    input_keyboard.append({"text": emj.news + " Latest news", "query": "c=news"})
    input_keyboard.append({"text": emj.plot + " Rankings", "query": "c=rankings"})

    if logged_in:
        input_keyboard.append({"text": emj.door + " Logout", "query": "c=logout"})

    keyboard = bot.get_keyboard(input_array=input_keyboard, grid=1)
    bot.send_message(text=text, message=message, con=controller,
                     keyboard=keyboard)
    
    
def get_callback(bot, call):
    _id = bot.get_id(call)
    bot.check_buff(call)
    dct = bot.get_data(call)

    command = dct.get('c')
    
    if command == 'main_menu':
        if dct.get('log') == 'False':
            main_menu(bot, call.message, controller="edit", logged_in=False)
        elif dct.get('log') == 'True':
            main_menu(bot, call.message, controller="edit", logged_in=True)
        
    elif command == 'login':
        request_login(bot, call.message)

    elif command == 'logout':
        logout(bot, call.message)
        
    elif command == 'profile':
        pass
    elif command == 'trades':
        pass
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

        # Check credentials
        print('checking credentials')
        if check_credentials(_login, _password, _id):
            bot.send_message(text="Account has been succesfully connected!", message=message)
            main_menu(bot, message, controller='send', logged_in=True)
        else:
            bot.send_message(text="Oops! Wrong login or password. Please try again.", message=message)
            main_menu(bot, message, controller='send', logged_in=False)
