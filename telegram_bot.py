import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import trader as trader
from subprocess import run
from tabulate import tabulate

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class telegram_bot():
    opened_trades=[]
    closed_trades=[]

    # Define a few command handlers. These usually take the two arguments update and
    # context. Error handlers also receive the raised TelegramError object in error.
    def start(self, update, context):
        update.message.reply_text("Trader running...")

    def analyze(self, update, context):
        update.message.reply_text("Analyzing...")
        self.opened_trades,self.closed_trades=trader.main()
        update.message.reply_text("Finished")
        
    def opened(self, update, context):
        result=str((tabulate(self.opened_trades, headers=['ID', 'Ticker','Open Date','Open'], tablefmt='simple')))
        update.message.reply_text(result)
    
    def closed(self, update, context):
        result=str((tabulate(self.closed_trades, headers=['ID', 'Ticker','Open Date','Open','Close Date','Close'], tablefmt='simple')))
        update.message.reply_text(result)
        
    def help(self, update, context):
        update.message.reply_text("Available options \n/start    : start trader\n/open    : show open trades\n/closed  : show closed trades\n/analyze : Open or close trades based on the analysis")

    def not_found(self, update, context):
        update.message.reply_text("Command not found")

    def error(self, update, context):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', self, update, context.error)

    def __init__(self):
        """Start the bot."""
        self.opened_trades,self.closed_trades=trader.main()
        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary
        updater = Updater("TOKEN", use_context=True)

        # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # Custom commands
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CommandHandler("help", self.help))
        dp.add_handler(CommandHandler("open", self.opened))
        dp.add_handler(CommandHandler("closed", self.closed))
        dp.add_handler(CommandHandler("analyze", self.analyze))

        # on noncommand i.e message - echo the message on Telegram
        dp.add_handler(MessageHandler(Filters.text, self.not_found))

        # log all errors
        dp.add_error_handler(self.error)

        # Start the Bot
        updater.start_polling()
    
        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()


if __name__ == '__main__':
    tb=telegram_bot()
