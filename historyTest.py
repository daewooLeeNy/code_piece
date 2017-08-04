import unittest
from code_reader import CodeReader
from finance_data_reader import history_yahoo, history_google, graph
from datetime import datetime

class historyTest(unittest.TestCase):
    def test_google_history(self):
        code_data = CodeReader().search_code('삼성전자');
        code = code_data['code.google'].values[0]

        data = history_google(code, datetime(2017, 1, 1), datetime.now())
        graph(data, code_data['company'].values[0])

    def test_yahoo_history(self):
        code_data = CodeReader().search_code('LG전자');
        code = code_data['code.yahoo'].values[0]

        data = history_yahoo(code, datetime(2017, 1, 1), datetime.now())
        graph(data, code_data['company'].values[0])
