from telegram.ext import Updater
from telegram.ext import  CommandHandler, MessageHandler, Filters
import  os
import json

#telegram token
TOKEN = "5228089500:AAGTi1w-EVUOMef5EbtRmwnjiadUC8_Pxw0"

#commandhandler for start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("""
    Available Commands:
    /help --> Get help
    /dict Your word here --> Online Dictionary
    """)

        
def Online_Dict(update: Update, context: CallbackContext):
    x = context.args[0]
    r = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{x}')
    data = json.loads(r.text)

    print("Your Word: " + data[0]['word'])
    dict_audio = ("audio: " + data[0]['phonetics'][0]['audio'])
    if len(dict_audio) ==0:
        update.message.reply_text("audio: " + data[0]['phonetics'][0]['audio'])
    else:
        update.message.reply_text("audio: " + data[0]['phonetics'][1]['audio'])

    update.message.reply_text(data[0]['meanings'][0]['definitions'][0]['definition'])
    try:
        update.message.reply_text(data[0]['meanings'][0]['definitions'][1]['definition'])
    except IndexError:
        print("")
        

def help(update: Update, context: CallbackContext):
    update.message.reply_text("You can waste your time here")


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)
  
  
def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)

#main logic
def main():
    
    #to get the updates from bot
    updater = Updater(token=TOKEN, use_context=True)
    
    #to dispatch the updates to respective handlers
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('dict', Online_Dict))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
    updater.dispatcher.add_handler(MessageHandler(
        # Filters out unknown commands
        Filters.command, unknown))

# Filters out unknown messages.
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))


     updater.dispatcher.add_error_handler(error)
    
    #to start webhook
    updater.start_webhook(listen="0.0.0.0",port=os.environ.get("PORT",443),
                          url_path=TOKEN,
                          webhook_url="https://omni--bot.herokuapp.com/"+TOKEN)
    updater.idle()

#start application with main function
if __name__ == '__main__':
    main()
