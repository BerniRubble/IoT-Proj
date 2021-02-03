from flask import Flask, render_template,request
import pandas as pd
import datetime
import numpy as np
from threading import Thread

app=Flask(__name__)
buffer=['']
columns=['id', 'locale', 'data' , 'time' ,'stato']
path_file="C:/Users/manub/Desktop/Università/MODENA/iot_3D/PROGETTO/Python/Server/dataset/dataset.csv"
dataset=pd.DataFrame(columns=columns)

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
@app.route('/level', methods=['POST'])
def levelManager():
    req=request.get_data().decode("utf-8")
    level=int(req[3])
    timestamp=datetime.datetime.now()

    try:
        dataset=pd.read_csv(path_file, sep=';')
    except:
        dataset = pd.DataFrame(columns=columns)

    timestamp.time()

    tupla= [req[0]+req[1]+req[2],'theHome',timestamp.date(),timestamp.time(),(level-1)]
    dataset.loc[len(dataset)] =tupla

    dataset.to_csv(path_file,sep=';', index=False)
    print(dataset)
    if level == 2:
        print("Sono nel primo livello")
    elif level== 3:
        print("Sono nel secondo livello")
    elif level==4:
        print("Sono nel terzo livello")
    #print(level)

    return 'OK'

class FlaskThread(Thread):
    def __init__(self, nome):
        Thread.__init__(self)
        self.nome=nome
        #self.durata=durata
    def run(self):
        app.run(host='127.0.0.1', port=8080)