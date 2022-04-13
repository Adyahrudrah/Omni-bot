from telegram.ext import Updater
from telegram.ext import  CommandHandler, MessageHandler, Filters
import json
import requests
import os
import time
import urllib

#telegram token
TOKEN = os.environ.get("API_KEY")

headers = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
bot = telegram.Bot(token=TOKEN)

def start(update, context):
    update.message.reply_text("It's movie time, Let's dive in!")


def imdb(update, context):
    se = context.args
    imdb_base_url = "https://yts.mx/api/v2/list_movies.json?query_term="
    imdb_r = requests.get(f"{imdb_base_url}{se}")
    status_code = imdb_r.status_code
    if status_code == 200:
        imdb_data = json.loads(imdb_r.text)
        if len(imdb_data['data']['movies']) ==1:
            imdb_title = imdb_data['data']['movies'][0]['title_long']
            movie_hash = imdb_data['data']['movies'][0]['torrents'][0]['hash']
            quality = imdb_data['data']['movies'][0]['torrents'][0]['quality']
            movie_type = imdb_data['data']['movies'][0]['torrents'][0]['type']
            movie_banner = imdb_data['data']['movies'][0]['medium_cover_image']
            update.message.reply_text(imdb_title)
            update.message.bot.send_photo(update.message.chat_id, movie_banner)
            enc_movie = urllib.parse.quote(imdb_title+quality+movie_type) 
            magnet = f'magnet:?xt=urn:btih:{movie_hash}&dn={enc_movie}+YTS.MX&tr=http://track.one:1234/announce&tr=udp://track.two:80&udp://glotorrents.pw:6969/announce&udp://tracker.opentrackr.org:1337/announce&udp://torrent.gresille.org:80/announce&udp://tracker.openbittorrent.com:80&udp://tracker.coppersurfer.tk:6969&udp://tracker.leechers-paradise.org:6969&udp://p4p.arenabg.ch:1337&udp://tracker.internetwarriors.net:1337'  
            headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer briefly',
            # Already added when you pass json= but not when you pass data=
            # 'Content-Type': 'application/json',
            }

            params = {
            'api_token': 'V134WkurdBj9CaZgjv0Fj67vO7zIZf02DLmbXJpTu8TjMDfbtTmKaN46BrH3'
            }

            json_data = {
            'url': f'{magnet}',
            'domain': 'tiny.one'
            }

            r = requests.post('https://api.tinyurl.com/create', headers=headers, params=params, json=json_data)
            data = json.loads(r.text)
            update.message.reply_text(data['data']['tiny_url'])

        else:    
            for x in range(1, len(imdb_data['data']['movies'])):
                imdb_title = imdb_data['data']['movies'][x]['title_long']
                movie_hash = imdb_data['data']['movies'][x]['torrents'][0]['hash']
                quality = imdb_data['data']['movies'][x]['torrents'][0]['quality']
                movie_type = imdb_data['data']['movies'][x]['torrents'][0]['type']
                movie_banner = imdb_data['data']['movies'][x]['medium_cover_image']
                update.message.reply_text(imdb_title)
                update.message.bot.send_photo(update.message.chat_id, movie_banner)
                enc_movie = urllib.parse.quote(imdb_title+quality+movie_type)
                magnet = f'magnet:?xt=urn:btih:{movie_hash}&dn={enc_movie}+YTS.MX&tr=http://track.one:1234/announce&tr=udp://track.two:80&udp://glotorrents.pw:6969/announce&udp://tracker.opentrackr.org:1337/announce&udp://torrent.gresille.org:80/announce&udp://tracker.openbittorrent.com:80&udp://tracker.coppersurfer.tk:6969&udp://tracker.leechers-paradise.org:6969&udp://p4p.arenabg.ch:1337&udp://tracker.internetwarriors.net:1337'
                headers = {
                'accept': 'application/json',
                'Authorization': 'Bearer briefly',
                # Already added when you pass json= but not when you pass data=
                # 'Content-Type': 'application/json',
                }

                params = {
                'api_token': 'V134WkurdBj9CaZgjv0Fj67vO7zIZf02DLmbXJpTu8TjMDfbtTmKaN46BrH3'
                }

                json_data = {
                'url': f'{magnet}',
                'domain': 'tiny.one'
                }

                r = requests.post('https://api.tinyurl.com/create', headers=headers, params=params, json=json_data)
                data = json.loads(r.text)
                update.message.reply_text(data['data']['tiny_url'])
                    
    else:
        print(imdb_r.status_code)
        update.message.reply_text("Try again")

def unknown_text(update, context):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)
  
def unknown(update, context):
    update.message.reply_text(
        "Sorry I can't recognize the command , you said '%s'" % update.message.text)

def error(update, context):
    context.bot.send_message(update.message.chat.id, error)

def main():
    
    #to get the updates from bot
    updater = Updater(token=TOKEN, use_context=True)

    #to dispatch the updates to respective handlers
    updater.dispatcher.add_handler(CommandHandler('Start', start))
    updater.dispatcher.add_handler(CommandHandler('imdb', imdb))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))
    updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    updater.dispatcher.add_error_handler(error)


#commandhandler for start command
    #to start webhook
    updater.start_webhook(listen="0.0.0.0",port=os.environ.get("PORT",443),
                          url_path=TOKEN,
                          webhook_url="https://omni--bot.herokuapp.com/"+TOKEN)
    updater.idle()

#start application with main function
if __name__ == '__main__':
    main()
