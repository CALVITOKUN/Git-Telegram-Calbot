import random
import string
import telebot

TOKEN = '' #TU TOKEN
bot = telebot.TeleBot(TOKEN)
contraseñas = {}  # Diccionario para almacenar contraseñas por ID de chat y propósito

def generar_contraseña(longitud: int) -> str:
    caracteres = string.ascii_letters + string.digits + string.punctuation
    contraseña_generada = ''.join(random.choice(caracteres) for _ in range(longitud))
    return contraseña_generada

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, '¡Hola! Soy tu bot generador de contraseñas aleatorias. Usa /generar [propósito] para obtener una nueva contraseña.')


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message,'Puedes interactuar conmigo usando la siguiente lista de comandos. Por ahora , solo respondo a /start , /help , /generar, /recordar, /listarcontraseñas')



@bot.message_handler(commands=['generar'])
def generar(message):
    # Obtener el propósito de la contraseña desde el mensaje
    propósito = message.text.replace('/generar', '').strip()

    if not propósito:
        bot.reply_to(message, 'Por favor, especifica el propósito para el que deseas generar la contraseña.')
        return

    longitud = 12
    nueva_contraseña = generar_contraseña(longitud)
    chat_id = message.chat.id

    # Almacenar la contraseña generada para el chat actual y propósito
    if chat_id not in contraseñas:
        contraseñas[chat_id] = {}
    if propósito not in contraseñas[chat_id]:
        contraseñas[chat_id][propósito] = []
    contraseñas[chat_id][propósito].append(nueva_contraseña)

    bot.reply_to(message, f'Tu nueva contraseña aleatoria para {propósito} es: {nueva_contraseña}')

@bot.message_handler(commands=['recordar'])
def recordar(message):
    # Obtener el propósito de la contraseña desde el mensaje
    propósito = message.text.replace('/recordar', '').strip()

    if not propósito:
        bot.reply_to(message, 'Por favor, especifica el propósito para el que deseas recordar las contraseñas antiguas.')
        return

    chat_id = message.chat.id

    # Verificar si hay contraseñas almacenadas para este chat y propósito
    if chat_id in contraseñas and propósito in contraseñas[chat_id] and contraseñas[chat_id][propósito]:
        contraseñas_antiguas = ', '.join(contraseñas[chat_id][propósito])
        bot.reply_to(message, f'Contraseñas antiguas generadas para {propósito}: {contraseñas_antiguas}')
    else:
        bot.reply_to(message, f'No se han generado contraseñas antiguas para {propósito}.')

@bot.message_handler(commands=['lista'])
def listar_contraseñas(message):
    chat_id = message.chat.id

    # Verificar si hay contraseñas almacenadas para este chat
    if chat_id in contraseñas and contraseñas[chat_id]:
        lista_contraseñas = []
        for propósito, contraseñas_propósito in contraseñas[chat_id].items():
            contraseñas_propósito_str = ', '.join(contraseñas_propósito)
            lista_contraseñas.append(f'{propósito}: {contraseñas_propósito_str}')

        mensaje = '\n'.join(lista_contraseñas)
        bot.reply_to(message, f'Contraseñas actuales:  \n{mensaje}')
    else:
        bot.reply_to(message, 'No hay contraseñas almacenadas actualmente.')

if __name__ == '__main__':
    bot.polling()
