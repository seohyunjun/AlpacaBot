
import os
import telegram
from telegram.ext import Updater, MessageHandler, Filters  # import modules
import load_data
import sys
import bot
# message reply function
def get_message(update, context):
    msg = update['message']['text']

    if '/stock' in msg:
        msg_sp = msg.split(' ')
        if len(msg_sp) > 3:
            for stock_name in msg_sp[1:]:
                stock_msg = load_data.messege(stock_name)
                update.message.reply_text(stock_msg)
        else:
            stock_name=msg_sp[1] 
            stock_msg = load_data.messege(stock_name)
            update.message.reply_text(stock_msg)
    if '/news' in msg:
        msg_sp = msg.split(' ')
        if len(msg_sp) > 3:
            for stock_name in msg_sp[1:]:
                stock_msg = load_data.news_message(stock_name)
                update.message.reply_text(stock_msg)
        else:
            stock_name=msg_sp[1] 
            stock_msg = load_data.news_message(stock_name)
            update.message.reply_text(stock_msg)
    if '/result' in msg:
        msg_sp = msg.split(' ')
        name = msg_sp[1]
        season = msg_sp[2]
        
        if len(msg_sp) >= 3:
            name = msg_sp[1]
            season = msg_sp[2]
        
            stock_msg = load_data.load_inv_list(name, season)
            update.message.reply_text(stock_msg)
        else:
            update.message.reply_text("Input Ex : /result [NAME] [SEASON]")

# message_handler = MessageHandler(Filters.text, get_message)
# updater.dispatcher.add_handler(message_handler)

# updater.start_polling(timeout=3, clean=True)
# updater.idle()``


StockBot = bot.StockBot()
StockBot.add_handler(Filters.text, get_message)
StockBot.start()


    
