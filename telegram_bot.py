from telegram.ext import Updater, CommandHandler
from threading import Thread


class Telegram:
    def __init__(self, api_token, crypto_api):
        print 'Telegram bot starting...'
        self.crypto_api = crypto_api
        self.watchlist = []

        self.updater = Updater(token=api_token)
        self.dispatcher = self.updater.dispatcher

        commands = [
            CommandHandler(['add'],             self.add_crypto,        pass_args=True),
            CommandHandler(['del', 'remove'],   self.remove_crypto,     pass_args=True),
            CommandHandler(['wl', 'watchlist'], self.show_watchlist)
        ]

        for command in commands:
            self.dispatcher.add_handler(command)
        
        self.updater.start_polling()
        print 'Telegram bot started. Polling for updates...'

    def add_crypto(self, bot, update, args):
        '''
        Adds crypto to watchlist
        '''

        print 'Add command (from: %s | args: %s)' % \
                (update.message.from_user.first_name, ','.join(args))

        result = ''

        if len(args) >= 1:
            args = [arg.upper() for arg in args]

            watching  = list(set(self.watchlist) & set(args))
            found     = list(set(self.crypto_api.coin_list) & \
                             set(args).difference(watching))
            not_found = list(set(args).difference(self.crypto_api.coin_list))
            
            if watching:
                result += 'Already watching %s. (%s)\n' % \
                            (('these cryptos' if len(watching) > 1 else 'this crypto'),
                            ', '.join(watching))

            if found:
                result += 'Added new %s to watchlist. (%s)\n' % \
                            (('cryptos' if len(found) > 1 else 'crypto'),
                            ', '.join(found))
                
            if not_found:
                result += 'Couldn\'t find %s. (%s)\n' % \
                            (('these cryptos.' if len(not_found) > 1 else 'this crypto.'),
                            ', '.join(not_found))

            for crypto in found:
                self.watchlist.append(crypto)
                self.watchlist.sort()

            if found:
                t = Thread(target=self.crypto_api.get_prices, args=(self.watchlist, ))
                t.start()
        else:
            result = 'Not enough arguments'
        
        bot.send_message(chat_id=update.message.chat_id, text=result)

    def remove_crypto(self, bot, update, args):
        '''
        Removes crypto to watchlist
        '''

        print 'Remove command (from: %s | args: %s)' % \
            (update.message.from_user.first_name, ','.join(args))

        result = ''

        if len(args) >= 1:
            args        = [arg.upper() for arg in args]
            found       = list(set(args) & set(self.watchlist))
            not_found   = list(set(args).difference(self.watchlist))

            if found:
                result += 'Removed %s from watchlist. (%s)\n' % \
                            (('these cryptos' if len(found) > 1 else 'this crypto'),
                            ', '.join(found))

            if not_found:
                result += 'Not currently watching %s. (%s)\n' % \
                            (('these cryptos' if len(not_found) > 1 else 'this crypto'),
                            ', '.join(not_found))

            for crypto in found:
                self.watchlist.remove(crypto)
                del self.crypto_api.prices[crypto]
        else:
            result = 'Not enough arguments'
        
        bot.send_message(chat_id=update.message.chat_id, text=result)
    
    def show_watchlist(self, bot, update):
        print 'Show watchlist command (from: %s)' % \
            (update.message.from_user.first_name)

        result = None
        
        if len(self.watchlist) > 0:
            result = 'Currently watching: %s' % (', '.join(self.watchlist))
        else:
            result = 'Currently not watching anything.'
        
        bot.send_message(chat_id=update.message.chat_id, text=result)