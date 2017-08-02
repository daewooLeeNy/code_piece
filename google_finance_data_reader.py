import pandas as pd
import pandas_datareader as pdr
from datetime import datetime
import matplotlib.pyplot as plt

start = datetime(2015, 1, 1)
end = datetime.now()

data = pdr.get_data_google('KRX:005930', start, end)
print(data)

data['Close'].plot(style='--')
pd.rolling_mean(data['Close'], 7).plot(lw=2)
plt.title('삼성전자')
plt.legend(['종가시세', '이동평균 7일']);
plt.show();
