import logging
from telegram.ext import Updater, CommandHandler, MessageHandler
from config import BOTKEY
from fk import FlaskThread


def start(update, context):
    update.message.reply_text('Ciao mondo!')
def help_command(update, context):
    update.message.reply_text(f'Ecco la lista dei comandi:\n'+
                              f'/start: per avviare il bot\n'+
                              f'/nomelocale: per scegliere il nome del locale\n'+
                              f'/cambialocale: per cambiare il locale attuale\n'+
                              f'/stop: per fermare il bot\n')
def botMain():
    global updater
    print("Sono Dentro")
    updater=Updater(BOTKEY, use_context=True) #Oggetto principale per la gestione del Bot
    dp=updater.dispatcher #Oggetto per l'aggiunta degli handler, un handler è una funzione che viene richiamata quando mi arrivano dei messaggi
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help",help_command))

    updater.start_polling() #Funzione non bloccante che attiva la ricezione dei messaggi da telegram
    updater.idle()#Funzione bloccante


#Server base, non ottimizzato in un nulla per vedere se tutto funziona




if __name__=='__main__':
    thread=FlaskThread("flask")
    thread.start()
    botMain()


