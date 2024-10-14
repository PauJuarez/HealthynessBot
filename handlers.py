import telebot
import json
import random
from db import registrar_usuario

# Cargar tips desde el archivo tips.json
def cargar_tips():
    try:
        with open('tips.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("El archivo tips.json no fue encontrado.")
        return {}

# Inicializa el bot aquí si lo necesitas
API_TOKEN = '7899050061:AAGP97C_rurt_4N9EhBBFUw-os6ift-XJVQ'
bot = telebot.TeleBot(API_TOKEN)

# Cargar los tips al iniciar el archivo
oficios_relevantes = cargar_tips()
user_oficios = {}  # Diccionario para guardar el oficio de cada usuario

@bot.message_handler(commands=['start'])
def start_handler(message):
    registrar_usuario(message.chat.id)  # Registrar el usuario
    welcome_text = f"¡Hola {message.from_user.first_name}! Soy tu bot de bienestar. Por favor, selecciona tu oficio."
    bot.send_message(message.chat.id, welcome_text)
    mostrar_menu_oficios(message.chat.id)

def mostrar_menu_oficios(chat_id):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for oficio in oficios_relevantes.keys():
        button = telebot.types.KeyboardButton(oficio.capitalize())
        markup.add(button)
    bot.send_message(chat_id, "Selecciona tu oficio:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text.lower() in oficios_relevantes.keys())
def oficio_selection_handler(message):
    oficio_seleccionado = message.text.lower()
    user_oficios[message.chat.id] = oficio_seleccionado  # Guardar el oficio del usuario
    bot.send_message(message.chat.id, f"¡Has seleccionado el oficio: {oficio_seleccionado.capitalize()}!")
    mostrar_menu_tips(message.chat.id)

def mostrar_menu_tips(chat_id):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_tips = telebot.types.KeyboardButton("Obtener Tips")
    button_serius_tips = telebot.types.KeyboardButton("Obtener Tips Serios")
    button_live_tips = telebot.types.KeyboardButton("Obtener Tips de Vida")
    button_info = telebot.types.KeyboardButton("Más Información")
    markup.add(button_tips, button_serius_tips, button_live_tips, button_info)
    bot.send_message(chat_id, "¿Qué te gustaría hacer ahora?", reply_markup=markup)

# Cambiar para obtener tips solo cuando se presiona el botón "Obtener Tips"
@bot.message_handler(func=lambda message: message.text == "Obtener Tips")
def obtener_tips_handler(message):
    oficio = user_oficios.get(message.chat.id)  # Obtener el oficio del diccionario
    tips = oficios_relevantes.get(oficio, [])
    
    if tips:
        tip_aleatorio = random.choice(tips)  # Seleccionar un tip aleatorio
        bot.send_message(message.chat.id, f"Aquí tienes un tip: {tip_aleatorio}")
    else:
        bot.send_message(message.chat.id, "Lo siento, no tengo tips para este oficio.")

# Manejador para obtener tips serios
@bot.message_handler(func=lambda message: message.text == "Obtener Tips Serios")
def obtener_serius_tips_handler(message):
    oficio = user_oficios.get(message.chat.id)  # Obtener el oficio del diccionario
    tips_serios = obtener_serius_tips(oficio)  # Obtener los tips serios según el oficio

    if tips_serios:
        tip_aleatorio = random.choice(tips_serios)  # Seleccionar un tip aleatorio
        bot.send_message(message.chat.id, f"Aquí tienes un tip serio: {tip_aleatorio}")
    else:
        bot.send_message(message.chat.id, "Lo siento, no tengo tips serios disponibles para este oficio.")

# Manejador para obtener tips de vida
@bot.message_handler(func=lambda message: message.text == "Obtener Tips de Vida")
def obtener_live_tips_handler(message):
    tips_vida = obtener_live_tips()  # Obtiene todos los tips de vida
    
    if tips_vida:
        tip_aleatorio = random.choice(tips_vida)  # Seleccionar un tip aleatorio
        bot.send_message(message.chat.id, f"Aquí tienes un tip de vida: {tip_aleatorio}")
    else:
        bot.send_message(message.chat.id, "Lo siento, no tengo tips de vida disponibles.")

@bot.message_handler(func=lambda message: message.text == "Más Información")
def info_handler(message):
    info_text = "Este es un bot de bienestar que te brinda consejos para tu oficio. Usa /start para comenzar."
    bot.reply_to(message, info_text)

# Funciones adicionales para obtener tips
def obtener_serius_tips(oficio):
    try:
        with open('SeriusTips.json', 'r', encoding='utf-8') as f:
            serious_tips_data = json.load(f)
            return serious_tips_data.get(oficio, [])  # Retorna los tips del oficio o una lista vacía
    except FileNotFoundError:
        print("El archivo SeriusTips.json no fue encontrado.")
        return []  # Retorna una lista vacía si no se encuentra el archivo

def obtener_live_tips():
    try:
        with open('LiveTips.json', 'r', encoding='utf-8') as f:
            live_tips_data = json.load(f)
            return [tip for tips in live_tips_data.values() for tip in tips]  # Aplana la lista de tips
    except FileNotFoundError:
        print("El archivo LiveTips.json no fue encontrado.")
        return []  # Retorna una lista vacía si no se encuentra el archivo
