import telebot
import sqlite3 as sql
from telebot import types

bot = telebot.TeleBot('5837723506:AAGIUh7wKcykAE_1vZDNP_1sZTQAOE4L_pI')

current_db = ''

#Создаем кнопки 
button_create_db = types.KeyboardButton('Создать БД')
button_connect_db = types.KeyboardButton('Подключиться к существующей БД')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(button_create_db)
    markup.add(button_connect_db)
    bot.send_message(message.chat.id, 'Привет! Давай начнем работу. Ты можешь добавлять, удалять, искать сотрудников и редактировать информацию о них.\n' + '/add - добавить сотрудника\n' + '/search - найти сотрудника', reply_markup=markup)
    
@bot.message_handler(commands=['add'])
def start_adding(message):
    bot.send_message(message.chat.id, 'Введите фамилию')
    bot.register_next_step_handler(message, get_surname)

def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.chat.id, 'Введите имя')
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    global name
    name = message.text
    bot.send_message(message.chat.id, 'Введите должность')
    bot.register_next_step_handler(message, get_post)

def get_post(message):
    global post
    post = message.text
    bot.send_message(message.chat.id, 'Введите проект')
    bot.register_next_step_handler(message, get_project)

def get_project(message):
    global project
    keyboard = types.InlineKeyboardMarkup()
    project = message.text
    but_yes = types.InlineKeyboardButton(text="Да", callback_data="but_yes")
    but_no = types.InlineKeyboardButton(text="Нет", callback_data="but_no")
    keyboard.add(but_yes)
    keyboard.add(but_no)
    
    bot.send_message(message.chat.id, 'Проверьте правильность введенных данных.\n' + 'Фамилия: ' + surname + '\n' + 'Имя: ' + name + '\n' + 'Должность: ' + post + '\n' + 'Проект: ' + project, reply_markup=keyboard)

@bot.message_handler(commands=['search'])
def start_searching(message):
    bot.send_message(message.chat.id, 'Введите фамилию или -')
    bot.register_next_step_handler(message, get_surname_search)

def get_surname_search(message):
    global search_surname
    search_surname = message.text
    bot.send_message(message.chat.id, 'Введите имя или -')
    bot.register_next_step_handler(message, get_name_search)

def get_name_search(message):
    global current_db
    con_current = sql.connect(current_db + '.db')
    cur_current = con_current.cursor()
    global search_name
    search_name = message.text
    if(search_surname != '-' and search_name != '-'):
        cur_current.execute("SELECT * FROM emp_projects WHERE surname == ? AND name == ?", (search_surname.lower().title(), search_name.lower().title()))
        rows = cur_current.fetchall()
        if(len(rows) == 0):
            bot.send_message(message.chat.id, 'Сотрудники не найдены')
        else:
            for row in rows:
                bot.send_message(message.chat.id, 'Фамилия: ' + row[1] + '\n' + 'Имя: ' + row[0] + '\n' + 'Отчество: ' +  row[2] + '\n' + 'Должность: ' + row[3] + '\n' + 'Проект: ' + row[4])
    elif(search_surname != '-' and search_name == '-'):
        cur_current.execute("SELECT * FROM emp_projects WHERE surname == ?", (search_surname.lower().title(), ))
        rows = cur_current.fetchall()
        if(len(rows) == 0):
            bot.send_message(message.chat.id, 'Сотрудники не найдены')
        else:
            for row in rows:
                bot.send_message(message.chat.id, 'Фамилия: ' + row[1] + '\n' + 'Имя: ' + row[0] + '\n' + 'Отчество' +  row[2] + '\n' + 'Должность: ' + row[3] + '\n' + 'Проект: ' + row[4])
    elif(search_surname == '-' and search_name != '-'):
        cur_current.execute("SELECT * FROM emp_projects WHERE name == ?", (search_name.lower().title(), ))
        rows = cur_current.fetchall()
        if(len(rows) == 0):
            bot.send_message(message.chat.id, 'Сотрудники не найдены')
        else:
            for row in rows:
                bot.send_message(message.chat.id, 'Фамилия: ' + row[1] + '\n' + 'Имя: ' + row[0] + '\n' + 'Отчество' +  row[2] + '\n' + 'Должность: ' + row[3] + '\n' + 'Проект: ' + row[4])
    else:
        bot.send_message(message.chat.id, 'Сотрудники не найдены')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if(message.text == 'Создать БД'):
        bot.send_message(message.chat.id, 'Введите название БД')
        bot.register_next_step_handler(message, create_db)
    elif(message.text == 'Подключиться к существующей БД'):
        bot.send_message(message.chat.id, 'Введите название БД')
        bot.register_next_step_handler(message, connect_db)
    else:
        bot.send_message(message.chat.id, "Привет, я могу помочь тебе с информацией о сотрудниках. Ты можешь добавлять, удалять, искать сотрудников и редактировать информацию о них.\n" + "/add - добавить сотрудника\n" + '/search - найти сотрудника')

def create_db(message):
    global db_name
    global current_db
    con_admin = sql.connect('admin.db')
    cur_admin = con_admin.cursor()
    db_name = message.text
    cur_admin.execute("SELECT db_name FROM admin WHERE db_name = ?", (db_name, ))
    row = cur_admin.fetchall()
    if(len(row) == 0):
        con_new = sql.connect(db_name + '.db')
        cur_new = con_new.cursor()
        cur_new.execute("CREATE TABLE IF NOT EXISTS emp_projects (`name` STRING, `surname` STRING, `second_name` STRING, `post` STRING, `project` STRING, `avatar` BLOB, `date_start` STRING)")
        con_new.commit()
        current_db = db_name
        bot.send_message(message.chat.id, 'Введите пароль')
        bot.register_next_step_handler(message, create_db_passwd)
    else:
        bot.send_message(message.chat.id, 'БД с таким названием уже существует. Выберите другое название или подключитесь к существующей.')
        bot.register_next_step_handler(message, start)

def create_db_passwd(message):
    global db_passwd
    db_passwd = message.text
    con_admin = sql.connect('admin.db')
    cur_admin = con_admin.cursor()
    cur_admin.execute("INSERT INTO admin VALUES(?, ?)", (db_name, db_passwd))
    con_admin.commit()

def connect_db(message):
    global connect_db_name
    con_admin = sql.connect('admin.db')
    cur_admin = con_admin.cursor()
    connect_db_name = message.text
    cur_admin.execute("SELECT db_name FROM admin WHERE db_name = ?", (connect_db_name, ))
    row = cur_admin.fetchall()
    if(len(row) == 0):
        bot.send_message(message.chat.id, 'БД с названием ' + connect_db_name + ' не существует. Попробуйте ввести другое название или создайте новую БД')
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Введите пароль')
        bot.register_next_step_handler(message, get_db_passwd)
    
def get_db_passwd(message):
    global connect_db_passwd
    global current_db
    con_admin = sql.connect('admin.db')
    cur_admin = con_admin.cursor()
    connect_db_passwd = message.text
    cur_admin.execute("SELECT * FROM admin WHERE db_name = ?", (connect_db_name, ))
    row = cur_admin.fetchall()
    if(str(row[0][1]) == connect_db_passwd):
        current_db = connect_db_name
    else:
        if(message.text == '/start'):
            bot.register_next_step_handler(message, start)
        else:
            bot.send_message(message.chat.id, 'Неверный пароль')
            bot.send_message(message.chat.id, 'Введите пароль')
            bot.register_next_step_handler(message, get_db_passwd)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global current_db
    if call.message:
        if call.data == "but_yes":
            con_current = sql.connect(current_db + '.db')
            cur_current = con_current.cursor()
            cur_current.execute("INSERT INTO emp_projects VALUES (?, ?, ?, ?, ?, ?, ?)", (name.lower().title(), surname.lower().title(), '', post.lower().title(), project.lower().title(), '', ''))
            con_current.commit()
            bot.answer_callback_query(call.id)
        if call.data == "but_no":
            bot.send_message(call.message.chat.id, 'Введите фамилию')
            bot.register_next_step_handler(call.message, get_surname)
            bot.answer_callback_query(call.id)


bot.infinity_polling()