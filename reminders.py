import telebot
import time

# Función para enviar recordatorios
def enviar_recordatorio(bot, chat_id):
    try:
        bot.send_message(chat_id, "¡Recuerda beber agua y tomarte un descanso!")
    except telebot.apihelper.ApiTelegramException as e:
        print(f"Error enviando mensaje a {chat_id}: {e}")

# Función para iniciar recordatorios periódicos
def iniciar_recordatorios(bot):
    chat_ids = []
    
    # Cargar chat_ids desde un archivo de usuarios
    with open('users.json', 'r') as f:
        chat_ids = [line.strip() for line in f.readlines()]

    while True:
        for chat_id in chat_ids:
            enviar_recordatorio(bot, chat_id)
        time.sleep(3600)  # Espera 1 hora
