import requests
import sys
import time
from gpiozero import LED
from threading import Thread

from crypto_api import CryptoAPI
from helpers import *
from lcd_controller import LCDController
from telegram_bot import Telegram

class Main:
    def __init__(self):
        self.config     = read_config()
        self.led        = LED(8)
        self.running    = True

        self.crypto_api = CryptoAPI()
        self.telegram   = Telegram(self.config['telegram_api_key'], self.crypto_api)
        self.lcd        = LCDController()


        self.telegram.config = self.config
        self.telegram.load_limits()
        self.crypto_api.get_coin_list()

        t_display = Thread(target=self.display_updater)
        t_display.start()

        t_prices = Thread(target=self.price_updater)
        t_prices.start() 

    def notify(self, crypto):
        print 'Price limit triggered! (%s is %s than %s%s)' % \
              (crypto, self.telegram.limits[crypto]['operator'], \
               self.telegram.limits[crypto]['value'], self.config['currency_symbol'])
        
        del self.telegram.limits[crypto]
        self.telegram.save_limits()

        # Flash LED. Will replace with speaker soon
        self.led.on()
        time.sleep(1)
        self.led.off()

    def price_updater(self):
        while self.running:
            # Combined watchlist and limits to be able to remove limits
            # even if the crypto isn't showing on the LCD
            combined = self.telegram.watchlist + self.telegram.limits.keys()
            self.crypto_api.get_prices(combined)
            
            limits_copy = self.telegram.limits.copy()

            for crypto in limits_copy:
                if crypto not in self.crypto_api.prices:
                    continue

                limit = limits_copy[crypto]
                price = self.crypto_api.prices[crypto][self.config['currency']]

                if  (limit['operator'] == 'greater' and price > limit['value']) or \
                    (limit['operator'] == 'less' and price < limit['value']):
                        self.notify(crypto)

            time.sleep(self.config['price_update_interval'])

    def display_updater(self):
        while self.running:
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
                        price = '%.2f%s' % (self.crypto_api.prices[item].values()[0],
                                            self.config['currency_symbol'])
                    else:
                        price = '-'
                    
                    text += '%s: %s\n' % (item, price)

                self.lcd.clear()
                self.lcd.message(text)
                time.sleep(self.config['display_update_interval'])

if __name__ == '__main__':
    while not internet_on():
        print 'No internet connection. Retrying in 5 seconds.'
        time.sleep(5)

    Main()