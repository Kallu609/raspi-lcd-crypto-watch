import json
import requests

URLS = {
    'coinlist': 'https://www.cryptocompare.com/api/data/coinlist/',
    'pricemulti': 'https://min-api.cryptocompare.com/data/pricemulti'
}


class CryptoAPI:
    def __init__(self):
        self.prices = {}
        self.coin_list = {}

    def get_prices(self, watchlist):
        url = "%s?fsyms=%s&tsyms=%s" % \
                (URLS['pricemulti'], ','.join(watchlist), 'USD')

        r = requests.get(url)
        data = json.loads(r.text)

        self.prices = data
        return self.prices

    def get_coin_list(self):
        print 'Retrieving coin list...'
        r = requests.get(URLS['coinlist'])
        data = json.loads(r.text)


        if data['Response'] == 'Success':
            self.coin_list = data['Data']
            print 'Found %s cryptos' % (len(self.coin_list))
            return self.coin_list
        else:
            raise Exception('Failed to retrieve coin list')