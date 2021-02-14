from flask import Flask, render_template,request
import pandas as pd
import datetime
import numpy as np
from threading import Thread

app=Flask(__name__)
buffer=['']
columns=['id', 'birra' ,'locale', 'anno', 'mese', 'giorno' ,'ora','minuti','secondi','stato']
columns2=['id','birra','locale']
path_file="C:/Users/benef/Desktop/UNIMORE/Progetto IoT/IoT-Proj/Server/dataset/dataset.csv"
path_file2="C:/Users/benef/Desktop/UNIMORE/Progetto IoT/IoT-Proj/Server/dataset/birre_locali.csv"
dataset=pd.DataFrame(columns=columns)
birre_locali=pd.DataFrame(columns=columns2)

'''
@app.route('/', methods=['GET'])
def home():
    print(buffer[0])
    return render_template('home.html', buffer=buffer[0])

@app.route('/', methods=['POST'])
def updateBuffer():
    buffer[0]=request.get_data().decode("utf-8")
    return 'OK'
    #render_template('id_page.html', buffer=buffer[0])
'''
def leggiDataset():
    try:
        dataset=pd.read_csv(path_file, sep=';')
        birre_locali=pd.read_csv(path_file2, sep=';')
    except:
        dataset = pd.DataFrame(columns=columns)
        birre_locali = pd.DataFrame(columns=columns2)

    return dataset, birre_locali

@app.route('/', methods=['GET'])
def homeDash():
    dataset,birre_locali=leggiDataset()

    locali=dataset['locale'].unique()
    return render_template('home.html', locali=locali)

@app.route('/dashboard', methods=['POST'])
def dashboardManager():
    locale=request.form['local']
    dataset,birre_locali=leggiDataset()
    dataset=dataset[dataset.locale==locale]
    result_birre=[]
    for id in dataset['id'].unique():
        tmp = dataset[dataset['id'] == id]
        stato="Quasi finita"
        if tmp['stato'].iloc[-1] == 1:
            stato="Pieno"
        elif tmp['stato'].iloc[-1] == 2:
            stato="Metà"

        result_birre.append({'birra':tmp['birra'].iloc[-1], 'livello':stato})


    return render_template('dashboard.html', result_birre=result_birre, locale=locale)
@app.route('/level', methods=['POST'])
def levelManager():
    req=request.get_data().decode("utf-8")
    level=int(req[3])
    timestamp=datetime.datetime.now()

    try:
        dataset=pd.read_csv(path_file, sep=';')
        birre_locali=pd.read_csv(path_file2, sep=';')
    except:
        dataset = pd.DataFrame(columns=columns)
        birre_locali = pd.DataFrame(columns=columns2)

    timestamp.time()

    #print(birre_locali.columns[0])

    tupla= [req[0]+req[1]+req[2],'birra','default',timestamp.year,timestamp.month, timestamp.day,timestamp.hour,timestamp.minute, timestamp.second,(level-1)]
    for i in range(len(birre_locali)):
        if birre_locali['id'].iloc[i] == tupla[0]:
            tupla[2]=birre_locali['locale'].iloc[i]
            tupla[1] = birre_locali['birra'].iloc[i]

    dataset.loc[len(dataset)] =tupla


    dataset.to_csv(path_file,sep=';', index=False)
    print(dataset)

    if level == 2:
        print("Sono nel primo livello")
    elif level== 3:
        print("Sono nel secondo livello")
    elif level==4:
        print("Sono nel terzo livello")


    return 'OK'

class FlaskThread(Thread):
    def __init__(self, nome):
        Thread.__init__(self)
        self.nome=nome
        #self.durata=durata
    def run(self):
        app.run(host='127.0.0.1', port=8080)