import json

# Función para registrar un usuario
def registrar_usuario(chat_id):
    # Cargar los chat_ids existentes para evitar duplicados
    try:
        with open('users.json', 'r') as f:
            existing_users = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        existing_users = []  # Si el archivo no existe, inicializa como vacío

    # Agregar el nuevo chat_id solo si no está en la lista
    if str(chat_id) not in existing_users:
        with open('users.json', 'a') as f:
            f.write(f"{chat_id}\n")  # Registra el chat_id en el archivo
        print(f"Usuario registrado: {chat_id}")
    else:
        print(f"El usuario {chat_id} ya está registrado.")

# Función para obtener tips según el oficio
def obtener_tips(oficio):
    with open('tips.json', 'r', encoding='utf-8') as f:
        tips = json.load(f)
    return tips.get(oficio, [])
# Función para obtener tips del archivo SeriusTips.json

def obtener_serius_tips(oficio):
    try:
        with open('SeriusTips.json', 'r', encoding='utf-8') as f:
            serious_tips_data = json.load(f)
            return serious_tips_data.get(oficio, [])  # Retorna los tips del oficio o una lista vacía
    except FileNotFoundError:
        print("El archivo SeriusTips.json no fue encontrado.")
        return []  # Retorna una lista vacía si no se encuentra el archivo

# Función para obtener tips del archivo LiveTips.json
def obtener_live_tips():
    try:
        with open('LiveTips.json', 'r', encoding='utf-8') as f:
            live_tips_data = json.load(f)
            # Retorna todos los tips como una lista
            return [tip for tips in live_tips_data.values() for tip in tips]  # Aplana la lista de tips
    except FileNotFoundError:
        print("El archivo LiveTips.json no fue encontrado.")
        return []  # Retorna una lista vacía si no se encuentra el archivo




# Función para actualizar el oficio (no se usa en este caso, pero aquí está para referencia)
def actualizar_oficio(chat_id, oficio):
    pass  # Puedes implementar lógica de actualización si es necesario
