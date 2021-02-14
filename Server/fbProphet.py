from fbprophet import Prophet
import fk
import pandas as pd
from fbprophet.plot import plot_plotly, plot_components_plotly
import sklearn

#leggo il dataset
df = fk.leggiDataset()

#fitto il dataset con prophet
m = Prophet()
m.fit(df)

#estende al futuro per 365 giorni
future = m.make_future_dataframe(periods=365)
future.tail()

forecast = m.predict(future)
'''
#modeling holiday
#creo un dataset per ogni festività che voglio analizzare
saintpatrick = pd.DataFrame({
  'holiday': 'Saint Patrick',
  'ds': pd.to_datetime(['2016-03-17', '2017-03-17', '2018-03-17', '2019-03-17', '2020-03-17', '2021-03-17']),
  'lower_window': 0,
  'upper_window': 1,
})

christmas = pd.DataFrame({
  'holiday': 'Christmas',
  'ds': pd.to_datetime(['2016-12-25', '2017-12-25', '2018-12-25', '2019-12-25', '2020-12-25', '2021-12-25']),
  'lower_window': 0,
  'upper_window': 1,
})

newyearseve = pd.DataFrame({
  'holiday': 'New Years Eve',
  'ds': pd.to_datetime(['2016-12-31', '2017-12-31', '2018-12-31', '2019-12-31', '2020-12-31', '2021-12-31']),
  'lower_window': 0,
  'upper_window': 1,
})

holidays = pd.concat((saintpatrick, christmas, newyearseve))

#faccio previsioni al futuro per quelle festività
m = Prophet(holidays=holidays)
forecast = m.fit(df).predict(future)


#in teoria dovrebbe farmi un grafico e una nuova tabella
forecast = forecast[(forecast['saintpatrick'] + forecast['chrismtas'] + forecast['newyearseve']).abs() > 0][
        ['ds', 'saintpatrick', 'christmas', 'newyearseve']][-10:]
        
'''

