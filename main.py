from handlers import bot
from reminders import iniciar_recordatorios

if __name__ == '__main__':
    # Inicia el bot en un hilo separado para los recordatorios
    import threading
    reminder_thread = threading.Thread(target=iniciar_recordatorios, args=(bot,))
    reminder_thread.start()

    # Inicia el bot
    bot.polling()
