from functools import partial
from telegram.ext import Updater, CommandHandler
import logging
import json

from commands.commands import commands

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

class Telegram:
    def __init__(self, api_token, crypto_api):
        print 'Telegram bot starting...'
        self.crypto_api = crypto_api
        self.watchlist = []
        self.limits = {}

        self.updater = Updater(token=api_token)
        self.dispatcher = self.updater.dispatcher

        for command in commands:
            func = partial(command[1], ctx=self)
            handler = CommandHandler(command[0], func, pass_args=command[2])
            self.dispatcher.add_handler(handler)
        
        self.updater.start_polling()
        print 'Telegram bot started. Polling for updates...'

    def clear_limits(self):
        with open(self.config['limits_file'], 'w') as f:
            self.limits = {}
            f.write(json.dumps(self.limits))
            print 'Cleared limits on %s' % self.config['limits_file']

    def save_limits(self):
        with open(self.config['limits_file'], 'w') as f:
            f.write(json.dumps(self.limits))
            print 'Saved limits to %s' % self.config['limits_file']

    def load_limits(self):
        try:
            with open(self.config['limits_file'], 'r') as f:
                self.limits = json.loads(f.read())
        except:
            self.limits = {}

        print 'Read %s limits from %s' % (len(self.limits), self.config['limits_file'])
