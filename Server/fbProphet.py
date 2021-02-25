from fbprophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt

columns=['id', 'birra' ,'locale', 'anno', 'mese', 'giorno' ,'ora','minuti','secondi','stato']
columns2=['id','birra','locale']
path_file="C:/Users/manub/Desktop/Università/MODENA/iot_3D/PROGETTO/Python/Server/dataset/dataset.csv"
path_file2="C:/Users/manub/Desktop/Università/MODENA/iot_3D/PROGETTO/Python/Server/dataset/birre_locali.csv"

def leggi_beer_dataset(id):
  try:
    beer_dataset = pd.read_csv(
      f"C:/Users/manub/Desktop/Università/MODENA/iot_3D/PROGETTO/Python/Server/dataset/birre/{id}.csv", sep=';')
  except:
    beer_dataset = pd.DataFrame(columns=['ds', 'y'])
  return beer_dataset


def fbP():
  try:
    dataset = pd.read_csv(path_file, sep=';')

  except:
    dataset = pd.DataFrame(columns=columns)

  try:
    birre_locali = pd.read_csv(path_file2, sep=';')
  except:
    birre_locali = pd.DataFrame(columns=columns2)


  locali=birre_locali['locale'].unique()


  for locale in locali:
    beer_dataset = pd.DataFrame(columns=['ds', 'y'])
    loc = dataset[dataset.locale == locale]
    ids = loc['id'].unique()
    for id in ids:
      birra=loc[loc.id == id]
      years=birra['anno'].unique()
      for y in years:
        year = birra[birra.anno == y]
        months = year['mese'].unique()
        for m in months:
          month = year[year.mese == m]
          days = month['giorno'].unique()
          for d in days:
            day = month[month.giorno == d]
            n_birre_tot=0

            #conto quante volte volte è avvenuto un cambiamento di stato, se cambia vuol dire che la birra è stata consumata
            #questo mi serve per prevedere i consumi
            for i in range(len(day)):
              if (i+1) < len(day):
                if day['stato'].iloc[i] != day['stato'].iloc[i+1]:
                    n_birre_tot =n_birre_tot+1


            tupla = [f"{y}-{m}-{d}",n_birre_tot]


            beer_dataset.loc[len(beer_dataset)] = tupla
            beer_dataset.drop_duplicates(inplace=True)
            beer_dataset.to_csv(f"C:/Users/manub/Desktop/Università/MODENA/iot_3D/PROGETTO/Python/Server/dataset/birre/{id}.csv", sep=';', index=False)


def make_image():
  try:
    dataset = pd.read_csv(path_file, sep=';')

  except:
    dataset = pd.DataFrame(columns=columns)


  ids = dataset['id'].unique()

  for id in ids:
    df = leggi_beer_dataset(id)
    df.dropna(axis=0, inplace=True)
    m = Prophet(daily_seasonality=True)
    m.fit(df)
    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)
    m.plot_components(forecast)
    plt.savefig(f"C:/Users/manub/Desktop/Università/MODENA/iot_3D/PROGETTO/Python/Server/static/images/{id}.png")





