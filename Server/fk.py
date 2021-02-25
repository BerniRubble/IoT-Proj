from flask import Flask, render_template,request
import pandas as pd
import datetime
import fbProphet
from threading import Thread

app=Flask(__name__)
buffer=['']
columns=['id', 'birra' ,'locale', 'anno', 'mese', 'giorno' ,'ora','minuti','secondi','stato']
columns2=['id','birra','locale']
path_file="C:/Users/manub/Desktop/Università/MODENA/iot_3D/PROGETTO/Python/Server/dataset/dataset.csv"
path_file2="C:/Users/manub/Desktop/Università/MODENA/iot_3D/PROGETTO/Python/Server/dataset/birre_locali.csv"
dataset=pd.DataFrame(columns=columns)
birre_locali=pd.DataFrame(columns=columns2)


def leggiDataset():
    try:
        dataset=pd.read_csv(path_file, sep=';')

    except:
        dataset = pd.DataFrame(columns=columns)

    try:
        birre_locali = pd.read_csv(path_file2, sep=';')
    except:
        birre_locali = pd.DataFrame(columns=columns2)

    return dataset, birre_locali

@app.route('/newBarrel', methods=['POST'])
def n_barrel():
    return render_template('newLocal.html', n_barrel=int(request.form['nBarrell']))

@app.route('/insertNewBarrel', methods=['POST'])
def new_beer():
    dataset,birre_locali=leggiDataset()
    n_barrel=request.form['n_barrel']

    for i in range(int(n_barrel)):
        tup=[request.form[f"id_barrel{i}"],request.form[f"beer{i}"],request.form[f"local{i}"]]
        birre_locali.loc[len(birre_locali)]=tup
    birre_locali.to_csv(path_file2, sep=';', index=False)
    return render_template('barrelSuccess.html')

@app.route('/', methods=['GET'])
def homeDash():
    dataset,birre_locali=leggiDataset()
    locali=dataset['locale'].unique()
    fbProphet.fbP()

    return render_template('home.html', locali=locali)

@app.route('/dashboard', methods=['POST'])
def dashboardManager():
    fbProphet.make_image()
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

        ids=dataset['id'].unique()
        birre=[]

        for id in ids:
            br=birre_locali[birre_locali.id == id]
            birre.append({'id': id, 'birra': br['birra'].iloc[0]})

    return render_template('dashboard.html', result_birre=result_birre, locale=locale,  birre=birre)

@app.route('/ordina', methods=['POST'])
def oderBeer():
    birra=request.form['birra']
    return render_template('newOrder.html',birra=birra)

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

    tupla= [req[0]+req[1]+req[2],'birra','default',timestamp.year,timestamp.month, timestamp.day,timestamp.hour,timestamp.minute, timestamp.second,(level-1)]
    #il livello è sottratto di 1 solo per chiarezza di lettura ed avere unqa corrispondeza tra primo livello=1, secondo livello=2, terzo livello=3
    for i in range(len(birre_locali)):
        if birre_locali['id'].iloc[i] == tupla[0]:
            tupla[2]=birre_locali['locale'].iloc[i]
            tupla[1] = birre_locali['birra'].iloc[i]

    dataset.loc[len(dataset)] =tupla

    dataset.to_csv(path_file,sep=';', index=False)

    #Le righe di codice successive mi servono solamente come controllo
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
    def run(self):
        app.run(host='0.0.0.0', port=8080)