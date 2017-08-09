#import json
from datetime import datetime

import simplejson as json
from code_reader import CodeReader
from flask import Flask
from flask_restful import Resource, Api, reqparse

from finance.finance_data_reader import history_google, history_yahoo

app = Flask(__name__)
api = Api(app)

codes_pd = CodeReader().load()

parser = reqparse.RequestParser()
parser.add_argument('q', type=str, help='종목 명칭')
parser.add_argument('provider', type=str, default='google', help="종가 제공처. google | yahoo")
parser.add_argument('start', type=str, default='20100101', help='조회 시작일')
parser.add_argument('end', type=str, default='now', help='조회 종료일')


class StockList(Resource):
    def get(self):
        args = parser.parse_args()

        result = None
        if args['q'] is None:
            result = codes_pd
        else:
            result = CodeReader.search_code(args['q'])

        return json.loads(result.to_json(orient="records", force_ascii=False))


class Stock(Resource):
    def get(self, code):
        company = codes_pd.ix[code]
        return json.loads(company.to_json(force_ascii=False))


class History(Resource):
    def get(self, code):
        args = parser.parse_args()
        provider = args['provider']
        start = self.convert_date(args['start'])
        end = self.convert_date(args['end'])
        stock_code = self.getCode(provider, code)

        histories = None
        if provider == "google":
            histories = history_google(stock_code, start, end)
        elif provider == "yahoo":
            histories = history_yahoo(stock_code, start, end)

        return json.loads(histories.to_json(date_format='iso', force_ascii=False))

    @classmethod
    def convert_date(cls, date_string):
        if date_string == 'now' or date_string is None:
            return datetime.now()
        else:
            return datetime.strptime(date_string, '%Y%m%d')

    @classmethod
    def getCode(cls, provider, code):
        company = codes_pd.ix[code]
        return company["code." + provider]


api.add_resource(StockList, '/stock')
api.add_resource(Stock, '/stock/<code>')
api.add_resource(History, '/stock/<code>/historical')


if __name__ == '__main__':
    app.run(debug=True)