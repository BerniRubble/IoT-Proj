import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.keyboardbutton import KeyboardButton
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from config import BOTKEY
import datetime
from fk import FlaskThread, path_file, columns
import pandas as pd


def start(update, context):
    print("Commando start ricevuto")
    update.message.reply_text('Ciao mondo!')
def help_command(update, context):
    print("Commando help ricevuto")
    update.message.reply_text(f'Ecco la lista dei comandi:\n'+
                              f'/start: per avviare il bot\n'+
                              f'/nomelocale: per scegliere il nome del locale\n'+
                              f'/cambialocale: per cambiare il locale attuale\n'+
                              f'/stop: per fermare il bot\n')
def local_name(update, context):
    print("Commando nomelocale ricevuto")
    update.message.reply_text(f'Ecco la lista dei locali:\n' +
                              f'/theHome\n')
def theHome(update,context):
    try:
        dataset=pd.read_csv(path_file, sep=';', parse_dates=['time'])
    except:
        dataset = pd.DataFrame(columns=columns)
    #print(dataset['time'].iloc[-1])
    local_thehome=dataset[dataset.locale == 'theHome']
    now_time = datetime.datetime.now()
    ids=local_thehome['id'].unique()
    for id in ids:
        tmp=local_thehome[local_thehome==id]
        if (now_time.time()-tmp['time'].iloc[-1]) > 0:
            update.message.reply_text(f'OFFERTAAAAAAAAAAAAAAAAA')
    update.message.reply_text(f'Hai selezionato il locale theHome\n'+
                              f'per cambiare usa: /cambialocale\n')

def botMain():
    global updater
    print("Sono Dentro")
    updater=Updater(BOTKEY, use_context=True) #Oggetto principale per la gestione del Bot
    dp=updater.dispatcher #Oggetto per l'aggiunta degli handler, un handler è una funzione che viene richiamata quando mi arrivano dei messaggi

    #handler messaggi
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help",help_command))
    dp.add_handler(CommandHandler("nomelocale",local_name))
    dp.add_handler(CommandHandler("cambialocale", local_name))
    dp.add_handler(CommandHandler("theHome", theHome))

    updater.start_polling() #Funzione non bloccante che attiva la ricezione dei messaggi da telegram
    updater.idle()#Funzione bloccante


#Server base, non ottimizzato in un nulla per vedere se tutto funziona




if __name__=='__main__':
    #Il servizio flask è in un thread
    # perchè il gestore di telegram deve stare per forza nel thread principale
    thread=FlaskThread("flask")
    thread.start()
    botMain()


