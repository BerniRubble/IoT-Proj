from fbprophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt

# path_file1 = "C:/Users/benef/Desktop/UNIMORE/Progetto IoT/IoT-Proj/Prophet/A01.csv"
path_file2 = "C:/Users/benef/Desktop/UNIMORE/Progetto IoT/IoT-Proj/Prophet/B01.csv"
path_file3 = "C:/Users/benef/Desktop/UNIMORE/Progetto IoT/IoT-Proj/Prophet/B02.csv"


def prophet():
    df1 = pd.read_csv(path_file2, sep=';')
    m = Prophet()
    m.fit(df1)
    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)
    m.plot_components(forecast)
    plt.savefig(f"C:/Users/benef/Desktop/UNIMORE/Progetto IoT/IoT-Proj/Prophet/B01.png")

    df2 = pd.read_csv(path_file3, sep=';')
    df = pd.concat([df1, df2])
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)
    m.plot_components(forecast)
    plt.savefig(f"C:/Users/benef/Desktop/UNIMORE/Progetto IoT/IoT-Proj/Prophet/BTavern.png")

    saintpatrick = pd.DataFrame({
        'holiday': 'saint patrick',
        'ds': pd.to_datetime(['2017-03-17', '2018-03-17', '2019-03-17', '2020-03-17']),
        'lower_window': 0,
        'upper_window': 1,
    })
    christmaseve = pd.DataFrame({
        'holiday': 'christmas eve',
        'ds': pd.to_datetime(['2017-12-24', '2018-12-24', '2019-12-24', '2020-12-24']),
        'lower_window': 0,
        'upper_window': 1,
    })
    holidays = pd.concat((saintpatrick, christmaseve))
    m = Prophet(holidays=holidays)
    forecast = m.fit(df).predict(future)
    m.plot_components(forecast)
    plt.savefig(f"C:/Users/benef/Desktop/UNIMORE/Progetto IoT/IoT-Proj/Prophet/holidays.png")


if __name__ == '__main__':
    prophet()
