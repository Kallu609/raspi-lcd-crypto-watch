class ShowWatchlist:
    def __init__(self, bot, update, ctx):
        print 'Show watchlist command (from: %s)' % \
            (update.message.from_user.first_name)
        
        self.ctx = ctx
        result = None
        
        if len(self.watchlist) > 0:
            result = 'Currently watching: %s' % (', '.join(self.watchlist))
        else:
            result = 'Currently not watching anything.'
        
        bot.send_message(chat_id=update.message.chat_id, text=result)
    
    def __getattr__(self, name):
        return getattr(self.ctx, name)