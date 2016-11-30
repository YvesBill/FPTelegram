# -*- coding: utf-8 -*-
import telegram
from datetime import datetime
from telegram.error import NetworkError, Unauthorized
from time import sleep
from random import randint
import re
import emoji

secondi_per_comporre_messaggio=5
secondi_per_reazione_a_messaggio=2

CARTELLA_AUDIO = "./audio/"
CARTELLA_IMMAGINI="./immagini/"

#bot = telegram.Bot('299756937:AAEtQEy5BFxQwKIun9--C6il4tTMRDZHAk0') #mazzoni_bot
botMAZZONI = telegram.Bot('316562823:AAHwslod-hSg1Zxk2zJgFx6ntmaM3yNzjeE') #mazzoniprovabot
botSTELLA = telegram.Bot('261195408:AAG6ZFN_bXD0qYXM6nu33jmiRJhvF-29X7w') #mazzoniprovabot
botIVAN = telegram.Bot('321203831:AAGwlLcerOyj2u_h8XlHKc4EUnovpq49_H8') #mazzoniprovabot
botING_BRUNO = telegram.Bot('329126191:AAFE_xFLMt-JitwM9WwCm-rek5Nkc_CpHR4') #mazzoniprovabot
botALONSO = telegram.Bot('306275959:AAHn7jaH5n26JRRaHo3K6M5TmHwUujz4uE8') #mazzoniprovabot
botRAIKKONEN = telegram.Bot('299938640:AAFby__wYPvEH4QCmzHja1TTQKi52x7zFvQ')
botVETTEL = telegram.Bot('326337719:AAGn3AatMCiNplY-gMcmTlbDigL_PGwzaN0')
botARRIVABENE = telegram.Bot('243076778:AAE8Cj6P5DfM5_4VcIjTWvIwQG6YRQ6eD78')
botBORTUZZO = telegram.Bot('194879571:AAFjP06lvg_TowUIwYzot2YcUrWcoc0wFkg')
botTOTO = telegram.Bot('246745177:AAFjWc2q47f14wkCUx9bDn3bbSpaexBAwCc')
botROSBERG = telegram.Bot('271080065:AAEYbz1i14Jq_ZrYSVUYJUMkE7y9F944p8s')
'''



'''

try:
	update_id = botMAZZONI.getUpdates()[0].update_id
	#print update_id
except IndexError:
	update_id = None

row=[]
keywords=[]
payload=[]
indices_found=[]
#f=codecs.open("tormentoni.txt","r","utf-8")
f=open("tormentoni.txt","r")
row = f.read().split("\n")
numero_tormentoni = len(row) -1
f.close()

#print row[0]

for i in range(numero_tormentoni):
	keywords.append(	row[i].split("\t")[0]	)
	arr = row[i].split("\t")
	payload.append(arr[1:])
#print payload[0]#[3]
#print payload[0][2]
#print payload[0][2].decode('utf-8')
#print payload[0][2].decode('string-escape').decode("utf-8")
def fakeHumanTyping(PERSONAGGIO,chat_id,FORMATO):
	cmd="sleep(0)"
	global secondi_per_reazione_a_messaggio
	global secondi_per_comporre_messaggio
	sleep(secondi_per_reazione_a_messaggio)
	if (FORMATO=="TXT"):
		cmd="bot" + PERSONAGGIO + ".sendChatAction(chat_id=chat_id,action=\"typing\")"
	if (FORMATO=="IMG"):
		cmd="bot" + PERSONAGGIO + ".sendChatAction(chat_id=chat_id,action=\"upload_photo\")"
	if (FORMATO=="DOCUMENT"):
		cmd="bot" + PERSONAGGIO + ".sendChatAction(chat_id=chat_id,action=\"upload_document\")"
	if (FORMATO=="MP3"):
		cmd="bot" + PERSONAGGIO + ".sendChatAction(chat_id=chat_id,action=\"upload_audio\")"
	#print cmd
	eval(cmd)
	sleep(secondi_per_comporre_messaggio)
	
def manda_messaggio_iesimo(PERSONAGGIO,FORMATO,PAYLOAD,chat_id):	
	if (FORMATO=="TXT"):
		#<bestemmie>
		#PAYLOAD può contenere sia EMOTICON che parole ACCENTATE e solo co sto stratagemma me le pesca tutte e due
		PAYLOAD = PAYLOAD.decode('utf-8').encode('unicode-escape').replace('\\\\', '\\').decode('unicode-escape') 
		#http://stackoverflow.com/questions/40640838/print-unicode-string-containing-both-accented-characters-and-emoticons/40641201?noredirect=1#comment68516872_40641201
		#</bestemmie>
		PAYLOAD = PAYLOAD.replace("<A CAPO>","\n")
		PAYLOAD=PAYLOAD.replace("'","\'")
	fakeHumanTyping(PERSONAGGIO,chat_id,FORMATO)
	if (FORMATO=="TXT"):
		cmd="bot" + PERSONAGGIO + ".sendMessage(chat_id=chat_id,parse_mode=\"Markdown\",text=PAYLOAD)"
		eval(cmd)
	if (FORMATO=="IMG"):
		f=open(CARTELLA_IMMAGINI + PAYLOAD,"rb")
		cmd="bot" + PERSONAGGIO + ".sendPhoto(chat_id=chat_id,photo=f)"
		#print cmd
		eval(cmd)
		f.close()
	if (FORMATO=="DOCUMENT"):
		f=open(PAYLOAD,"rb")
		cmd="bot" + PERSONAGGIO + ".sendDocument(chat_id=chat_id,document=f)"
		eval(cmd)
		f.close()
	if (FORMATO=="STICKER"):
		cmd="bot" + PERSONAGGIO + ".sendSticker(chat_id=chat_id,sticker=PAYLOAD)"
		eval(cmd)
	if (FORMATO=="MP3"):
		f=open(CARTELLA_AUDIO + PAYLOAD,"rb")
		cmd="bot" + PERSONAGGIO + ".sendVoice(chat_id=chat_id,voice=f)"
		#print cmd
		eval(cmd)
		f.close()

def manda_tutto_il_thread_di_messaggi(chat_id,casuale):
	for i in range(len(payload[casuale])/3):
		PERSONAGGIO=payload[casuale][3*i]
		FORMATO=payload[casuale][3*i + 1]
		PAYLOAD=payload[casuale][3*i + 2]
		#print PERSONAGGIO,FORMATO,PAYLOAD
		manda_messaggio_iesimo(PERSONAGGIO,FORMATO,PAYLOAD,chat_id)
		
def echo(botMAZZONI):
	global update_id
	for update in botMAZZONI.getUpdates(offset=update_id, timeout=10):
		try:
			chat_id = update.message.chat_id
		except AttributeError:
			print "abort"
		update_id = update.update_id + 1

		try:
			try:
				if update.message.new_chat_member:  # your bot can receive updates without messages
					new_user = update.message.new_chat_member
					botMAZZONI.sendMessage(chat_id = chat_id, text ="Un cordiale saluto a " + new_user.first_name + " da Gianfranco Mazzoni e Ivan Capelli")
			except:
				continue
		
			if update.message.text:  # your bot can receive updates without messages
				#print update.message.text
				del indices_found[:]
				for i in range(numero_tormentoni):
					if (	(" " + keywords[i] + " ") in (" " +	update.message.text.upper()	+ " ")	) or (	(" " + keywords[i] + "") in (" " +	update.message.text.upper()	+ " ")	) or (	("" + keywords[i] + " ") in (" " +	update.message.text.upper()	+ " ")	): #se bingo
						indices_found.append(i)
						
				if len(indices_found)>0:
					casuale = indices_found[	randint(0,len(indices_found)-1)	]
					#print "casuale:" + str(casuale)
					per_non_essere_troppo_ripetitivo = randint(1, 10)
					if per_non_essere_troppo_ripetitivo > 3:
						manda_tutto_il_thread_di_messaggi(chat_id,casuale)
		except IndexError:
			print "attrerr"
			continue

while True:
	try:
		echo(botMAZZONI)
	except NetworkError:
		sleep(1)
	except Unauthorized:
		update_id += 1
