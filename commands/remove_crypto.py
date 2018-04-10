class RemoveCrypto:
    def __init__(self, bot, update, args, ctx):
        print 'Remove command (from: %s | args: %s)' % \
            (update.message.from_user.first_name, ','.join(args))
        
        self.ctx = ctx
        result = ''

        if not len(args) >= 1:
            result = 'Not enough arguments'
            bot.send_message(chat_id=update.message.chat_id, text=result)
            return

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
        
        bot.send_message(chat_id=update.message.chat_id, text=result)

    def __getattr__(self, name):
        return getattr(self.ctx, name)