from telegram import *
from telegram.ext import *
import json
import requests
import os
import telegram
import urllib.parse

#telegram token
TOKEN = os.environ.get("API_KEY")
TOKEN_TINY_URL = os.environ.get("API_KEY_TINY")

headers = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
bot = telegram.Bot(token=TOKEN)

def start(update, context):
    user_name = update.effective_chat.username
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hello {user_name} ❤️")

def Help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
    text=f"Looking for a Movie? Click this command to copy 👉 `/Search Interstellar`",  parse_mode=telegram.ParseMode.MARKDOWN)

def Search(update, context): 
    try:
        q = context.args
        if not q:
            context.bot.send_message(chat_id=update.message.chat_id, text=f"*Use /Search command to find a movie to get download id.", 
            parse_mode=telegram.ParseMode.MARKDOWN)
        else:    
            se = urllib.parse.quote(" ".join(q))
            yts_img_url = "https://yts.mx/api/v2/list_movies.json?query_term="
            yts_url = f"{yts_img_url}{se}"
            yts_r = requests.get(yts_url)
            status_code_yts = yts_r.status_code
            if status_code_yts == 200:
                yts_data = json.loads(yts_r.text)
                for x in range(0, len(yts_data['data']['movies'])):      
                    banner_title = yts_data['data']['movies'][x]['title_english']
                    banner_year = yts_data['data']['movies'][x]['year']
                    banner_rating = yts_data['data']['movies'][x]['rating']
                    banner_img = yts_data['data']['movies'][x]['large_cover_image']
                    banner_id = yts_data['data']['movies'][x]['id']
                    banner_text = "Title: "+banner_title+" Year: "+str(banner_year)+ " IMDB rating: "+str(banner_rating)
                    banner_yt_trailer_id = yts_data['data']['movies'][x]['yt_trailer_code']
                    update.message.bot.send_photo(update.message.chat_id, banner_img)
                    update.message.reply_text(banner_text)
                    update.message.reply_text("https://www.youtube.com/embed/"+banner_yt_trailer_id)
                    context.bot.send_message(chat_id=update.message.chat_id, text=f"*Click to copy* 👉`/Download {banner_id}`.", 
                    parse_mode=telegram.ParseMode.MARKDOWN)
            if status_code_yts == 525:
                update.message.reply_text(f"🤖: Sever Down😭")
    except KeyError as e:
        qErr = " ".join(q)
        update.message.reply_text(f"🤖: {qErr} 404! Item Not found 😭")
    except TypeError:
        update.message.reply_text(f"🤖: {se} not found 😭")
    except IndexError:
        context.bot.send_message(chat_id=update.message.chat_id, text=f"*Use /Search command to find a movie to get download id.", 
                parse_mode=telegram.ParseMode.MARKDOWN)
    except ValueError:
        context.bot.send_message(chat_id=update.message.chat_id, text=f"*Use /Search command to find a movie to get download id.", 
                parse_mode=telegram.ParseMode.MARKDOWN)
    except Exception as e:
        context.bot.send_message(chat_id=update.message.chat_id, text=f"*Click to copy* 👉 eg. `/Search Interstellar`.", 
                parse_mode=telegram.ParseMode.MARKDOWN)

def Download(update, context):
    try:
        q = context.args
        if not q:
            context.bot.send_message(chat_id=update.message.chat_id, text=f"*Use /Search command to find a movie to get download id.", 
                parse_mode=telegram.ParseMode.MARKDOWN)
        else:        
            se = urllib.parse.quote(" ".join(q)) 
            imdb_base_url = "https://yts.mx/api/v2/movie_details.json?movie_id="
            imdb_r = requests.get(f"{imdb_base_url}{se}")
            status_code = imdb_r.status_code
            if status_code == 200:
                imdb_data = json.loads(imdb_r.text)
                imdb_title = imdb_data['data']['movie']['title_long']
                imdb_torrents = imdb_data['data']['movie']['torrents']
                for i in range(0, len(imdb_torrents)):
                    movie_hash = imdb_data['data']['movie']['torrents'][i]['hash']
                    movie_type = imdb_data['data']['movie']['torrents'][i]['type']
                    movie_quality = imdb_data['data']['movie']['torrents'][i]['quality']
                    movie_size = imdb_data['data']['movie']['torrents'][i]['size']
                    if movie_quality == "720p":
                        enc_movie = urllib.parse.quote(imdb_title+movie_quality+movie_type) 
                        magnet = f'magnet:?xt=urn:btih:{movie_hash}&dn={enc_movie}+YTS.MX&tr=udp://track.two:80&udp://open.demonii.com:1337/announce&udp://tracker.openbittorrent.com:80&udp://tracker.coppersurfer.tk:6969&udp://glotorrents.pw:6969/announce&udp://tracker.opentrackr.org:1337/announce&udp://torrent.gresille.org:80/announce&udp://p4p.arenabg.com:1337&udp://tracker.leechers-paradise.org:6969'
                        json_data = {'url': f'{magnet}','domain': 'tiny.one'}
                        headers = {'accept': 'application/json','Content-Type' : 'application/json'}
                        params = {'api_token': TOKEN_TINY_URL}
                        r = requests.post('https://api.tinyurl.com/create', headers=headers, params=params, json=json_data)
                        data = json.loads(r.text)
                        tin_url = data['data']['tiny_url']
                        ch_name = [[InlineKeyboardButton('uTorrent', url=f"{tin_url}")]]
                        reply_markup = InlineKeyboardMarkup(ch_name)
                        context.bot.send_message(chat_id=update.message.chat.id, text=f"{imdb_title}: 720p ~ {movie_size}",
                        reply_markup = reply_markup)
                    if movie_quality == "1080p":
                        enc_movie = urllib.parse.quote(imdb_title+movie_quality+movie_type) 
                        magnet = f'magnet:?xt=urn:btih:{movie_hash}&dn={enc_movie}+YTS.MX&tr=udp://track.two:80&udp://open.demonii.com:1337/announce&udp://tracker.openbittorrent.com:80&udp://tracker.coppersurfer.tk:6969&udp://glotorrents.pw:6969/announce&udp://tracker.opentrackr.org:1337/announce&udp://torrent.gresille.org:80/announce&udp://p4p.arenabg.com:1337&udp://tracker.leechers-paradise.org:6969'
                        json_data = {'url': f'{magnet}','domain': 'tiny.one'}
                        headers = {'accept': 'application/json','Content-Type' : 'application/json'}
                        params = {'api_token': TOKEN_TINY_URL}
                        r = requests.post('https://api.tinyurl.com/create', headers=headers, params=params, json=json_data)
                        data = json.loads(r.text)
                        tin_url = data['data']['tiny_url']
                        ch_name = [[InlineKeyboardButton('uTorrent', url=f"{tin_url}")]]
                        reply_markup = InlineKeyboardMarkup(ch_name)
                        context.bot.send_message(chat_id=update.message.chat.id, text=f"{imdb_title}: 1080p ~ {movie_size}",
                        reply_markup = reply_markup)
        if status_code == 525:
            update.message.reply_text("🤖: Drink a cup ♨️ of tea and come back")
    except TypeError:
        update.message.reply_text(f"🤖: {se} not found 😭")
    except IndexError:
        context.bot.send_message(chat_id=update.message.chat_id, text=f"*Use /Search command to find a movie to get download id.", 
                parse_mode=telegram.ParseMode.MARKDOWN)
    except ValueError:
        context.bot.send_message(chat_id=update.message.chat_id, text=f"*Use /Search command to find a movie to get download id.", 
                parse_mode=telegram.ParseMode.MARKDOWN)
    except Exception as e:
        context.bot.send_message(chat_id=update.message.chat_id, text=f"*Find a movie to download Click to copy* 👉eg. `/Search Gravity`.", 
                parse_mode=telegram.ParseMode.MARKDOWN)
    

def unknown_text(update, context):
#     update.message.reply_text("Sorry I can't recognize you , you said '%s'" % update.message.text)
try:
        q = context.args
        if not q:
            context.bot.send_message(chat_id=update.message.chat_id, text=f"*Use /Search command to find a movie to get download id.", 
            parse_mode=telegram.ParseMode.MARKDOWN)
        else:    
            se = urllib.parse.quote(" ".join(q))
            yts_img_url = "https://yts.mx/api/v2/list_movies.json?query_term="
            yts_url = f"{yts_img_url}{se}"
            yts_r = requests.get(yts_url)
            status_code_yts = yts_r.status_code
            if status_code_yts == 200:
                yts_data = json.loads(yts_r.text)
                for x in range(0, len(yts_data['data']['movies'])):      
                    banner_title = yts_data['data']['movies'][x]['title_english']
                    banner_year = yts_data['data']['movies'][x]['year']
                    banner_rating = yts_data['data']['movies'][x]['rating']
                    banner_img = yts_data['data']['movies'][x]['large_cover_image']
                    banner_id = yts_data['data']['movies'][x]['id']
                    banner_text = "Title: "+banner_title+" Year: "+str(banner_year)+ " IMDB rating: "+str(banner_rating)
                    banner_yt_trailer_id = yts_data['data']['movies'][x]['yt_trailer_code']
                    update.message.bot.send_photo(update.message.chat_id, banner_img)
                    update.message.reply_text(banner_text)
                    update.message.reply_text("https://www.youtube.com/embed/"+banner_yt_trailer_id)
                    context.bot.send_message(chat_id=update.message.chat_id, text=f"*Click to copy* 👉`/Download {banner_id}`.", 
                    parse_mode=telegram.ParseMode.MARKDOWN)
            if status_code_yts == 525:
                update.message.reply_text(f"🤖: Sever Down😭")
    except KeyError as e:
        qErr = " ".join(q)
        update.message.reply_text(f"🤖: {qErr} 404! Item Not found 😭")
    except TypeError:
        update.message.reply_text(f"🤖: {se} not found 😭")
    except IndexError:
        context.bot.send_message(chat_id=update.message.chat_id, text=f"*Use /Search command to find a movie to get download id.", 
                parse_mode=telegram.ParseMode.MARKDOWN)
    except ValueError:
        context.bot.send_message(chat_id=update.message.chat_id, text=f"*Use /Search command to find a movie to get download id.", 
                parse_mode=telegram.ParseMode.MARKDOWN)
    except Exception as e:
        context.bot.send_message(chat_id=update.message.chat_id, text=f"*Click to copy* 👉 eg. `/Search Interstellar`.", 
                parse_mode=telegram.ParseMode.MARKDOWN)

def error(update, context):
    context.bot.send_message(update.message.chat.id, error)

def main():
    updater = Updater(token=TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('Download', Download))
    updater.dispatcher.add_handler(CommandHandler('Search', Search))
    updater.dispatcher.add_handler(CommandHandler('Help', Help))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))
    updater.dispatcher.add_error_handler(error)

#commandhandler for start command
    #to start webhook
    updater.start_webhook(listen="0.0.0.0",port=os.environ.get("PORT",443),
                          url_path=TOKEN,
                          webhook_url="https://binge-bot.herokuapp.com/"+TOKEN)
    updater.idle()

#start application with main function
if __name__ == '__main__':
    main()
