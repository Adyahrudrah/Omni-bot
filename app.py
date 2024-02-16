import re
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import requests
from bs4 import BeautifulSoup
import langcodes
import iso639
import json





TMDb_API_KEY = "0e008146a88193a6bd377fa6fec83993"
TMDB_BASE_URL = "https://api.themoviedb.org/3/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

async def fetchPoster(search_query, movie_type):
    search_url = f"{TMDB_BASE_URL}search/{movie_type}?api_key={TMDb_API_KEY}&query={search_query}"
    try:
        response = requests.get(search_url)
        response.raise_for_status()  
        data = response.json()
        if data.get('results'):
            first_tv_show = data['results'][0]
            poster_path = first_tv_show.get('poster_path')
            if poster_path:
                poster_url = f"https://image.tmdb.org/t/p/w185{poster_path}"
                return poster_url
            else:
                print('None')
                return None
        else:
            try:
                if (movie_type != 'tv'):
                    return await fetchPoster(search_query, 'tv')
            except:
                return None
    except requests.exceptions.RequestException as e:
        print('None')
        return None
        
def text_to_language_code(language_name):
    try:
        language_code = langcodes.Language.find(language_name).to_alpha3()
        language_code = iso639.to_iso639_1(language_code)
        return language_code
    except:
        return 'en'
    
        
        
async def ia(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    language = text_to_language_code(context.args[0]) if context.args else 'ta' 
    count = context.args[1] if context.args else 10
    IMDb_url = f'https://www.imdb.com/search/title/?title_type=feature&sort=moviemeter,asc&primary_language={language}&count={count}'
    response = requests.get(IMDb_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        containers = soup.find_all(class_='ipc-metadata-list-summary-item')
        try: 
            for container in containers:
                title = container.find(class_='ipc-title').text.strip()
                title = re.sub(r'^\d+\.\s', '', title)
                
                year = container.find_all(class_= 'fcCUPU')[0].text.strip()
                poster = container.find(class_='ipc-image').get('src')
                
                try:
                    number_of_votes_element = container.find(class_='ipc-rating-star--voteCount')
                    number_of_votes = number_of_votes_element.text.strip()
                except:
                    number_of_votes = ''
                    
                try:
                    rating_element = container.find(class_='ipc-rating-star')
                    rating = rating_element.text.split('(')[0].strip()
                except:
                    rating = ''
                    
                message = f'Title: {title}\nYear: {year}\nVotes: {number_of_votes}\nRating: {rating}'
                if poster:
                    await update.message.reply_photo(photo=poster, caption=message)
                else:
                    await update.message.reply_text(message)

        except Exception as e:
            print(e)


    
async def lm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    sorted_links = []
    tbl_url = 'https://www.1tamilblasters.zip/'
    response = requests.get(tbl_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        movie_links = soup.find_all('a')
        for movie_link in movie_links:
            movie_link = movie_link
            if movie_link:
                match = re.search(r'(.*)\(\d{4}\)', movie_link.text.strip())
                if match:
                    sorted_links.append(movie_link)
    if sorted_links:
        sorted_links = sorted_links[0:3]  
        for sorted_link in sorted_links:
            movie_title = re.search(r'(.*)\(\d{4}\)', sorted_link.text.strip()).group()
            movie_url = sorted_link.get('href')
            movie_url_response = requests.get(movie_url, headers=headers)
            if movie_url_response.status_code == 200:
                soup = BeautifulSoup(movie_url_response.text, 'html.parser')
                magnet_link = soup.find(class_='magnet-plugin')
                if magnet_link:
                    magnet_link = magnet_link.get('href')
                    poster = await fetchPoster(re.sub(r'\((\d{4})\)', '\1', movie_title), 'movie')
                    if poster:
                        await update.message.reply_photo(photo=poster, caption=movie_title)
                    else:
                        await update.message.reply_text(movie_title)
    


def main():
    app = ApplicationBuilder().token("5474453546:AAHhDOfAyg2E2dwRHOMvrtm-GiAtFNAol2Q").build()
    app.add_handler(CommandHandler("ia", ia))
    app.add_handler(CommandHandler("lm", lm))
    app.run_polling()


if __name__ == "__main__":
    main()
