from telegram import ParseMode
from threading import Thread

class AddCrypto:
    def __init__(self, bot, update, args, ctx):
        print 'Add command (from: %s | args: %s)' % \
                (update.message.from_user.first_name, ','.join(args))

        self.ctx = ctx
        result = ''

        if not len(args) >= 1:
            result = '*Error*: Not enough arguments'
            return bot.send_message(chat_id=update.message.chat_id, \
                                    text=result, \
                                    ParseMode=MARKDOWN)

        args = [arg.upper() for arg in args]

        watching  = list(set(self.watchlist) & set(args))
        found     = list(set(self.crypto_api.coin_list) & \
                            set(args).difference(watching))
        not_found = list(set(args).difference(self.crypto_api.coin_list))
        

        if found:
            result += '*Success*: Added new %s to watchlist. (%s)\n' % \
                        (('cryptos' if len(found) > 1 else 'crypto'),
                        ', '.join(found))

        if watching:
            result += '*Error*: Already watching %s. (%s)\n' % \
                        (('these cryptos' if len(watching) > 1 else 'this crypto'),
                        ', '.join(watching))
    
        if not_found:
            result += '*Error*: Couldn\'t find %s. (%s)\n' % \
                        (('these cryptos.' if len(not_found) > 1 else 'this crypto.'),
                        ', '.join(not_found))

        for crypto in found:
            self.watchlist.append(crypto)
            self.watchlist.sort()

        if found:
            t = Thread(target=self.crypto_api.get_prices, args=(self.watchlist, ))
            t.start()
        
        bot.send_message(chat_id=update.message.chat_id, text=result, \
                         parse_mode=ParseMode.MARKDOWN)
    
    def __getattr__(self, name):
        return getattr(self.ctx, name)