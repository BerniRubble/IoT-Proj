import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.keyboardbutton import KeyboardButton
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from config import BOTKEY
import datetime
from fk import FlaskThread, path_file, columns, Thread
import time
from multiprocessing import Process
import fbProphet


#ths = []
phs=[]

'''
class localThread(Thread):
    def __init__(self, nome, up, idchat):
        Thread.__init__(self)
        self.locale = nome
        self.updater = up
        self.idChat = idchat
        self.stop=False
        #self.update = update
    def stop(self,stop):
        self.stop=stop
    def run(self):
        print("Thread partito")
        while True:
            try:
                dataset = pd.read_csv(path_file, sep=';')
            except:
                dataset = pd.DataFrame(columns=columns)
            locale = dataset[dataset.locale == self.locale]
            date_now = datetime.datetime.now()
            for id in locale['id'].unique():
                tmp=locale[locale['id']==id]
                if tmp['stato'].iloc[-1] != 3:
                    if date_now.year == tmp['anno'].iloc[-1]: #altrimenti è scaduta
                        if (date_now.month - tmp['mese'].iloc[-1]) < 1: #altrimenti è scaduta
                            if len(tmp) >10:
                                cont=0
                                #Questo ciclo mi serve per controllare che i
                                #le dieci rilevazioni precedenti siano nello stesso stato e quindi deve andare in offerta
                                for i in range(11):
                                    if i == 0 or i==1:
                                        pass
                                    else:
                                        if tmp['stato'].iloc[-i] == tmp['stato'].iloc[-1]:
                                            cont=cont+1
                                if cont==9:
                                    self.updater.bot.send_message(chat_id=self.idChat,
                                                                  text=f"la birra {tmp['birra'].iloc[-1]} è in offerta",
                                                                  timeout=15)
                                    time.sleep(5)


'''

def bot_process(loc,idc):
    print("Thread partito")
    exit_process = False
    while exit_process==False:
        try:
            dataset = pd.read_csv(path_file, sep=';')
        except:
            dataset = pd.DataFrame(columns=columns)
        locale = dataset[dataset.locale == loc]
        date_now = datetime.datetime.now()
        for id in locale['id'].unique():
            tmp = locale[locale['id'] == id]
            if tmp['stato'].iloc[-1] != 3:
                if date_now.year == tmp['anno'].iloc[-1]:  # altrimenti è scaduta
                    if (date_now.month - tmp['mese'].iloc[-1]) < 1:  # altrimenti è scaduta
                        if len(tmp) > 10:
                            cont = 0
                            # Questo ciclo mi serve per controllare che i
                            # le dieci rilevazioni precedenti siano nello stesso stato e quindi deve andare in offerta
                            for i in range(11):
                                if i == 0 or i == 1:
                                    pass
                                else:
                                    if tmp['stato'].iloc[-i] == tmp['stato'].iloc[-1]:
                                        cont = cont + 1
                            if cont == 9:
                                updater.bot.send_message(chat_id=idc,
                                                         text=f"la birra {tmp['birra'].iloc[-1]} è in offerta",
                                                         timeout=1)
                                #time.sleep(5)
                                exit_process=True




'''
def start(update, context):
    print("Commando start ricevuto")

    chatId = update.effective_chat.id
    print(chatId)

    update.message.reply_text('Benvenuto nel nostro bot usa il comando /help per vedere i comandi disponibili')
    

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
    

#Funzioni per la gestione dei locali

'''

def start(update,context):
    #update.message.reply_text(f'Hai selezionato il locale theHome\n'+
      #                         f'per cambiare usa: /cambialocale\n')
    chatId = update.effective_chat.id
    #th=localThread("theHome", updater, chatId)
    #th.start()
    #ths.append(th)
    ph=Process(target=bot_process("theHome",chatId))
    ph.start()
    phs.append(ph)


def stop(update, context):
    print("Comando Stop attivato")
    #exit_process=True
    for p in phs:
        p.terminate()
        print(f"Stopping ..... {p}")

def botMain():
    global updater

    updater=Updater(BOTKEY, use_context=True) #Oggetto principale per la gestione del Bot
    dp=updater.dispatcher #Oggetto per l'aggiunta degli handler, un handler è una funzione che viene richiamata quando mi arrivano dei messaggi

    #handler messaggi
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stop", stop))

    '''
    dp.add_handler(CommandHandler("help",help_command))
    dp.add_handler(CommandHandler("nomelocale",local_name))
    dp.add_handler(CommandHandler("cambialocale", local_name))
    dp.add_handler(CommandHandler("theHome", theHome))
    '''
    updater.start_polling() #Funzione non bloccante che attiva la ricezione dei messaggi da telegram
    updater.idle()#Funzione bloccante






if __name__=='__main__':
    #Il servizio flask è in un thread
    # perchè il gestore di telegram deve stare per forza nel thread principale
    thread=FlaskThread("flask")
    thread.start()
    botMain()



