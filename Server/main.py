
from telegram.ext import Updater, CommandHandler
from config import BOTKEY
import datetime
from fk import FlaskThread, path_file, columns, columns2, Thread
import pandas as pd


class localThread(Thread):
    def __init__(self, nome, up, idchat):
        self.loc = nome
        self.updater = up
        self.idc = idchat
        Thread.__init__(self)


    def run(self):

        print("Thread partito")
        exit_process = False
        while exit_process==False:
            try:
                dataset = pd.read_csv(path_file, sep=';')
            except:
                dataset = pd.DataFrame(columns=columns)

            locale = dataset[dataset.locale == self.loc]
            date_now = datetime.datetime.now()

            for identifier in locale['id'].unique():
                tmp = locale[locale['id'] == identifier]
                if tmp['stato'].iloc[-1] != 3:
                    if date_now.year == tmp['anno'].iloc[-1]:  # altrimenti è scaduta
                        if (date_now.month - tmp['mese'].iloc[-1]) < 1:  # altrimenti è scaduta
                            if len(tmp) > 10:
                                cont = 0
                                # Questo ciclo mi serve per controllare che
                                # le dieci rilevazioni precedenti siano nello stesso stato e quindi deve andare in offerta
                                #Utilizziamo solo 10 rilevazioni per questione di simulazione
                                for i in range(11):
                                    if i == 0 or i == 1:
                                        pass
                                    else:
                                        if tmp['stato'].iloc[-i] == tmp['stato'].iloc[-1]:
                                            cont = cont + 1

                                if cont >= 9:
                                    self.updater.bot.send_message(chat_id=self.idc,text=f"la birra {tmp['birra'].iloc[-1]} è in offerta nel locale {tmp['locale'].iloc[-1]}",timeout=1)
                                    exit_process=True
                else:
                    if (date_now.day - tmp['giorno'].iloc[-1]) < 1:
                        self.updater.bot.send_message(chat_id=self.idc,
                                                      text=f"OPS!!! la birra {tmp['birra'].iloc[-1]} è in FINITA nel locale {tmp['locale'].iloc[-1]}",
                                                      timeout=1)

                        exit_process = True

        print("Ho finito")




def start(update,context):
    chatId = update.effective_chat.id

    try:
        dataset = pd.read_csv(path_file, sep=';')
    except:
        dataset = pd.DataFrame(columns=columns2)

    for locale in dataset['locale'].unique():
        if locale != "default":
            ph=localThread(locale,updater,chatId)
            ph.start()





def botMain():
    global updater

    updater=Updater(BOTKEY, use_context=True) #Oggetto principale per la gestione del Bot
    dp=updater.dispatcher #Oggetto per l'aggiunta degli handler, un handler è una funzione che viene richiamata quando mi arrivano dei messaggi

    #handler messaggi
    dp.add_handler(CommandHandler("start", start))


    updater.start_polling() #Funzione non bloccante che attiva la ricezione dei messaggi da telegram
    updater.idle()#Funzione bloccante


if __name__=='__main__':
    #Il servizio flask è in un thread
    #perchè il gestore di telegram deve stare per forza nel thread principale
    thread=FlaskThread("flask")
    thread.start()
    botMain()


