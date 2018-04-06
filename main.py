import json
import requests
import sys
import time
import urllib2
from gpiozero import LED
from threading import Thread

from crypto_api import CryptoAPI
from lcd_controller import LCDController
from telegram_bot import Telegram

def read_config():
    with open('config.json', 'r') as f:
        return json.loads(f.read())

def chunks(l, n):
    """Yield succesive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]

def internet_on():
    try:
        urllib2.urlopen('http://216.58.192.142', timeout=3)
        return True

    except urllib2.URLError as err:
        return False

class Main:
    def __init__(self):
        self.crypto_api = CryptoAPI()
        self.telegram   = Telegram(config['telegram_api_key'], self.crypto_api)
        self.lcd        = LCDController()

        self.limits = {
            'BTC': {
                'type': 'greater',
                'value': 6000
            }
        }
        
        print 'Retrieving coin list...'
        self.crypto_api.get_coin_list()
        print 'Found %s cryptos' % (len(self.crypto_api.coin_list))

        t_display = Thread(target=self.update_display)
        t_display.start()

        t_price_updater = Thread(target=self.update_prices)
        t_price_updater.start() 

    def notify(self, crypto):
        print 'Price limit triggered! (%s)' % (crypto)
        
        del self.limits[crypto]

        # Flash LED. Will replace with speaker soon
        led.on()
        time.sleep(1)
        led.off()

    def update_prices(self):
        while True:
            self.crypto_api.get_prices(self.telegram.watchlist)

            for crypto in self.limits:
                if crypto not in self.crypto_api.prices:
                    continue

                limit = self.limits[crypto]
                price = self.crypto_api.prices[crypto]
                
                if limit['type'] == 'greater':
                    if price > limit['value']:
                        self.notify(crypto)

                if limit['type'] == 'less':
                    if price < limit['value']:
                        self.notify(crypto)

            time.sleep(config['price_update_interval'])

    def update_display(self):
        try:
            while True:
                if len(self.telegram.watchlist) == 0:
                    self.lcd.clear()
                    self.lcd.message('Please add\ncrypto(s)')
                    time.sleep(1)
                    continue

                for chunk in chunks(self.telegram.watchlist, 2):
                    text = ''

                    for item in chunk:
                        price = None

                        if item in self.crypto_api.prices:
                            price = '%.2f%s' % (self.crypto_api.prices[item].values()[0], config['currency_symbol'])
                        else:
                            price = '-'
                        
                        text += '%s: %s\n' % (item, price)

                    self.lcd.clear()
                    self.lcd.message(text)
                    time.sleep(config['display_update_interval'])

        except KeyboardInterrupt:
            print 'bye!'
            sys.exit()
            return

config = read_config()
led = LED(8)

while not internet_on():
    print 'No internet connection. Retrying in 10 seconds.'
    time.sleep(10)

if __name__ == '__main__':
    Main()