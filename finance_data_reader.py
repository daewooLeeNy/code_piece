from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as pdr

from code_reader import CodeReader


def history_google(code, start, end):
    return pdr.get_data_google(code, start, end)

def history_yahoo(code, start, end):
    return pdr.get_data_yahoo(code, start, end)

def graph(data, title):
    data['Close'].plot(style='--')
    pd.rolling_mean(data['Close'], 7).plot(lw=2)
    plt.title(title)
    plt.legend(['종가시세', '이동평균 7일']);
    plt.show();

if __name__ == "__main__":
    code_data = CodeReader().search_code('카카오');
    code = code_data['code.google'].values[0]

    data = history_google(code, datetime(2017, 1, 1), datetime.now())
    graph(data, code_data['company'].values[0])

