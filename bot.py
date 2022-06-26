import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler # import modules

def sendMessage(msg):
    bot = telegram.Bot(token = "5274317648:AAHRSonZ5zRBNIyx6KRMtzDPFL1bC5_yGQY")
    bot.sendMessage(chat_id=1909064563, text = msg)
    print("Send Message")
    return True

class TelegramBot:
    def __init__(self, name, Token):
        self.core = telegram.Bot(Token)
        self.updater = Updater(Token)
        self.id = 1909064563
        self.name = name
    def sendMessage(self, text):
        self.core.sendMessage(chat_id = self.id, text=text)
    def stop(self):
        self.updater.start_polling()
        self.updater.dispatcher.stop()
        self.updater.job_queue.stop()
        self.updater.stop()
    
class StockBot(TelegramBot):
    def __init__(self):
        self.Token = "5274317648:AAHRSonZ5zRBNIyx6KRMtzDPFL1bC5_yGQY"
        TelegramBot.__init__(self,'stockbot',self.Token)
        self.updater.stop()
    
    def add_handler(self, cmd, func):
        self.updater.dispatcher.add_handler(MessageHandler(cmd,func))

    def start(self):
        self.sendMessage("Start StockBot")
        self.updater.start_polling(timeout=3, clean=True)
        self.updater.idle()