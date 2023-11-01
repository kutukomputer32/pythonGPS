# mengimport package pyTelegramBotAPI
import telebot, json
import subprocess

# inisialisasi Token Bot
bot = telebot.TeleBot('6685750122:AAE3rPQEupZjWTE6o3QaeF1YEOUYMfcoMLo')
default_chat_id = 5981475588

def lokasi():
	result = subprocess.run(['./termux-location'], stdout=subprocess.PIPE).stdout
	result_json = json.loads(result)
	latitude = result_json['latitude']
	longitude = result_json['longitude']
	print(f'latitude: {latitude} longitude: {longitude}')
	return latitude, longitude

# Menghandle Pesan /start
@bot.message_handler(commands=['start'])
def welcome(message):
	# membalas pesan
	if message.chat.id != default_chat_id:
		print('failed: chat id not valid')
		return

	#bot.reply_to(message, message.chat.id)
	bot.reply_to(message, 'Halo, apa kabar?')

# Menghandle Pesan /lokasi
@bot.message_handler(commands=['lokasi'])
def kirim_lokasi(message):
	# membalas pesan
	if message.chat.id != default_chat_id:
		print('failed: chat id not valid')
		return

	#bot.reply_to(message, message.chat.id)
	bot.reply_to(message, 'Mendapatkan lokasi...')

	latitude, longitude = lokasi()

	bot.send_location(default_chat_id, latitude, longitude)

	#http://www.google.com/maps/place/

# Menghandle Pesan /info
@bot.message_handler(commands=['info'])
def info(message):
	# membalas pesan
	if message.chat.id != default_chat_id:
		print('failed: chat id not valid')
		return

	bot.reply_to(message, 'Informasi Perangkat\nTipe perangkat: Ponsel\nNama perangkat: MI A1')

# Menghandle Pesan /rickroll
@bot.message_handler(commands=['rickroll'])
def info(message):
	# membalas pesan
	if message.chat.id != default_chat_id:
		print('failed: chat id not valid')
		return

	bot.reply_to(message, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ')

while True:
	try:
		bot.polling()
	except:
		pass
