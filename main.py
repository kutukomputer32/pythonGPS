# mengimport package pyTelegramBotAPI
import telebot, json, keyboard
import subprocess, os

# inisialisasi Token Bot
bot = telebot.TeleBot('6685750122:AAE3rPQEupZjWTE6o3QaeF1YEOUYMfcoMLo')
default_chat_id = 5981475588

users = [5981475588]

def verify_user(chat_id):
	for user in users:
		if chat_id == user:
			print(user)
			return False

	return True

def extract_arg(arg):
    return arg.split(' ')[1]

def lokasi():
	print('starting termux-location...')
	result = subprocess.run(['./termux-location'], stdout=subprocess.PIPE).stdout
	print('get JSON')
	result_json = json.loads(result)
	print('get latitude and longitude information')
	latitude = result_json['latitude']
	longitude = result_json['longitude']
	print(f'latitude: {latitude} longitude: {longitude}')
	return latitude, longitude

# Menghandle Pesan /start
@bot.message_handler(commands=['start'])
def welcome(message):
	# membalas pesan
	if verify_user(message.chat.id):
		print('failed: chat id not valid')
		return

	#bot.reply_to(message, message.chat.id)
	bot.reply_to(message, 'Halo, apa kabar?')

# Menghandle Pesan /lokasi
@bot.message_handler(commands=['location', 'lokasi'])
def kirim_lokasi(message):
	# membalas pesan
	if verify_user(message.chat.id):
		print('failed: chat id not valid')
		return

	#bot.reply_to(message, message.chat.id)
	bot.reply_to(message, 'Mendapatkan lokasi...')

	latitude, longitude = lokasi()

	bot.send_location(message.chat.id, latitude, longitude)

	#http://www.google.com/maps/place/

# Menghandle Pesan /rickroll
@bot.message_handler(commands=['record'])
def record(message):
	# membalas pesan
	if verify_user(message.chat.id):
		print('failed: chat id not valid')
		return

	print('send audio...')

	arg = extract_arg(message.text)

	print('debug arg: ' + arg)

	if arg == 'start':
		os.system(f'termux-microphone-record -f record.mp3')
	elif arg == 'stop':
		os.system(f'termux-microphone-record -q')
	elif arg == 'send':
		bot.reply_to(message, 'send audio...')
		bot.send_audio(chat_id=message.chat.id, audio=open('record.mp3', 'rb'))
	else:
		bot.reply_to(message, 'Command not found.')

# Menghandle Pesan /battery
@bot.message_handler(commands=['battery', 'baterai'])
def battery(message):
	# membalas pesan
	if verify_user(message.chat.id):
		print('failed: chat id not valid')
		return

	bot.reply_to(message, 'Mendapatkan informasi baterai...')
	result = subprocess.run(['./termux-battery-status'], stdout=subprocess.PIPE).stdout
	print('get JSON')
	result_json = json.loads(result)
	bot.reply_to(message, f'Informasi Baterai\npersentase: {result_json["percentage"]}\nstatus: {result_json["status"]}\nsuhu: {result_json["temperature"]}')

# Menghandle Pesan /torch
@bot.message_handler(commands=['torch', 'senter'])
def torch(message):
	# membalas pesan
	if verify_user(message.chat.id):
		print('failed: chat id not valid')
		return

	arg = extract_arg(message.text)

	os.system(f'termux-torch {arg}')

	bot.reply_to(message, 'Berhasil menyalakan/mematikan senter')

# Menghandle Pesan /vibrate
@bot.message_handler(commands=['vibrate', 'getar'])
def vibrate(message):
	# membalas pesan
	if verify_user(message.chat.id):
		print('failed: chat id not valid')
		return

	os.system('termux-vibrate')

	bot.reply_to(message, 'Berhasil menggetarkan ponsel')

# Menghandle Pesan /volume
@bot.message_handler(commands=['volume'])
def vibrate(message):
	# membalas pesan
	if verify_user(message.chat.id):
		print('failed: chat id not valid')
		return

	arg = extract_arg(message.text)

	os.system(f'termux-vibrate {arg}')

	bot.reply_to(message, f'Berhasil mengubah volume menjadi {arg}')

# Menghandle Pesan /info
@bot.message_handler(commands=['info'])
def info(message):
	# membalas pesan
	if verify_user(message.chat.id):
		print('failed: chat id not valid')
		return

	bot.reply_to(message, 'Informasi Perangkat\nTipe perangkat: Ponsel\nNama perangkat: MI A1')

# Menghandle Pesan /rickroll
@bot.message_handler(commands=['rickroll'])
def rickroll(message):
	# membalas pesan
	if verify_user(message.chat.id):
		print('failed: chat id not valid')
		return

	bot.reply_to(message, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ')

'''
# Menghandle Pesan /exit
@bot.message_handler(commands=['help', 'bantuan'])
def help(message):
	# membalas pesan
	if verify_user(message.chat.id):
		print('failed: chat id not valid')
		return

	bot.reply_to(message, 'Command list\nlocation/lokasi - Mendapatkan lokasi\n')
'''

# Menghandle Pesan /exit
@bot.message_handler(commands=['exit', 'keluar'])
def bot_exit(message):
	# membalas pesan
	if verify_user(message.chat.id):
		print('failed: chat id not valid')
		return

	bot.reply_to(message, 'exit...')
	os.system('killall python3')

while True:
	try:
		bot.polling()
	except:
		pass
