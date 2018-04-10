from telegram import ParseMode
from helpers import *

class Limit:
    def __init__(self, bot, update, args, ctx):
        '''Example:
        /limit btc > 1000'''

        print 'Limit command (from: %s | args: %s)' % \
                (update.message.from_user.first_name, ','.join(args))

        self.ctx = ctx
        result = ''

        if len(args) == 0:
            result += '*Currently notifying when*\n'

            if not self.limits:
                result += '_Never_'
            
            for limit in self.limits:
                result += '`1 %s` is %s than `%.2f%s`\n' % (limit, \
                           self.limits[limit]['operator'], \
                           self.limits[limit]['value'], \
                           self.config['currency_symbol'])
        
        elif len(args) == 1 and args[0].lower() == 'clear':
            self.clear_limits()
            result = '*Clear*: Notify list is cleared.'
        
        elif not args[0].upper() in self.crypto_api.coin_list:
            result = '*Error*: \'%s\' is not a valid crypto.' % args[0]

        elif not args[1] in ['>', '<']:
            result = '*Error*: Second parameter should be > or <'

        elif not isFloat(args[2]):
            result = '*Error*: Second parameter should be > or <'

        elif len(args) < 3:
            result = '*Error*: Not enough arguments'

        elif len(args) > 3:
            result = '*Error*: Too many arguments'

        else:
            crypto   = args[0].upper()
            operator = 'greater' if args[1] == '>' else 'less'
            value    = float(args[2])
            
            self.limits[crypto] = {
                'operator': operator,
                'value'   : value
            }

            self.save_limits()

            result = '*Success*: Notifying when `1 %s` is %s than `%.2f%s`' % \
                     (crypto, operator, value, read_config()['currency_symbol'])

        bot.send_message(chat_id=update.message.chat_id, text=result, \
                         parse_mode=ParseMode.MARKDOWN)

    def __getattr__(self, name):
        return getattr(self.ctx, name)