import pandas as pd


class CodeReader():
    filename = 'korea_stock_code.csv'
    data = None

    @classmethod
    def load(self, filename=None):
        if filename is None:
            filename = self.filename

        ## code 값에 leading 0 유지 후 index 처리
        self.data = pd.read_csv(filename, comment='#', converters={'code': lambda x: str(x)})
        self.data = self.data.set_index('code', drop=False)
        return self.data;

    @classmethod
    def search_code(self, company):
        if self.data is None:
            self.load()

        return self.data[self.data['company'].str.contains(company)]


if __name__ == "__main__":
    data = CodeReader().search_code('삼성전자');
    print(data);
