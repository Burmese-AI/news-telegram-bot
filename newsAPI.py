import os
from dotenv import load_dotenv, find_dotenv
import json
import worldnewsapi.api_client
import worldnewsapi.configuration
from worldnewsapi.models.top_news200_response import TopNews200Response
from worldnewsapi.rest import ApiException
from random import choice
import requests

#LOAD API KEY
load_dotenv(find_dotenv())
KEY = os.getenv("API_KEY")

def fetch_lan_code(code):
    try:
        with open("country_code.json", 'r') as countryCodes:
            country_data = json.load(countryCodes)
            for country, country_code in country_data.items():
                if code == country_code:
                    country_name = country
        
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        if FileNotFoundError:
            print("File not found.\n")

        else:
            print("Could not encode JSON file.\n")
    
    try:
        with open("language_code.json", "r") as lanCodes:
            lan_data = json.load(lanCodes)
            return lan_data[country_name]
    
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        if FileNotFoundError:
            print("File not found.\n")
        
        else:
            print("Could not encode JSON file.\n")

#FETCH TOP NEWS USING COUNTRY CODES AND LANGUAGE CODES
def fetch_TopNews(country_code, language_code):
    url = f"https://api.worldnewsapi.com/top-news?source-country={country_code}&language={language_code}"

    headers = {
        'x-api-key': KEY
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        new_data = response.json()
        top_news = []
        for category in new_data.get("top_news", [])[:1]:
            for news in category.get("news", [])[:10]:
                top_news.append(
                    {
                        "Title": news['title'],
                        "URL": news['url'],
                        "Publish_date": news['publish_date'],
                        "Author": news['author'] if news['author'] else None
                    }
                )
        return top_news

    else:
        return f"Error: {response.status_code}"


#SEARCH NEWS USING NEW TOPICS
def search_news(topic):
    url = f"https://api.worldnewsapi.com/search-news?text={topic}&language=en&number=10"

    headers = {
        'x-api-key': KEY
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        new_data = response.json()
        news = [
            {
                "Title": new['title'],
                "URL": new['url'],
                "Publish_date": new['publish_date'],
                "Author": new['author'] if new['author'] else None
            } for new in new_data.get("news", [])
        ]
        return news

    else:
        return f"Error: {response.status_code}"

#EXTRACT ONE RANDOM NEW FROM THE GIVEN TOPIC   
def search_random(topic):
    url = f"https://api.worldnewsapi.com/search-news?text={topic}&language=en&number=10"

    headers = {
        'x-api-key': KEY
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        new_data = response.json()
        rand_news = choice(new_data["news"])
        if rand_news:
            random_new = [
                {
                    "Title": rand_news.get('title'),
                    "URL": rand_news.get('url'),
                    "Publish_date": rand_news.get('publish_date'),
                    "Author": rand_news.get('author' if rand_news.get('author') else None)
                }
            ]
            return random_new
            # print(random_new)

    else:
        return f"Error: {response.status_code}"

"""!!!!__DANGER ZONE__!!!!
DEAR TIMMY,
!!!DO NOT TOUCH THE CODE BELOW OR YOU WILL REGRET YOUR LIFE DECISION.

"""

# def main():
#     country = str.lower((input("Can you write the name of the country you want?\n")))
#     language_code = fetch_lan_code(country)
#     fetch_TopNews(country, language_code)

# def search():
#     topic = str.lower(input("Enter a topic: ")).replace(' ', '+')
#     search_random(topic)

# def fetch_country_code(country):
#     try:
#         with open("country_code.json", 'r') as codes:
#             data = json.load(codes)
#             return data[country]
        
#     except (FileNotFoundError, json.decoder.JSONDecodeError):
#         if FileNotFoundError:
#             print("File not found.\n")

#         else:
#             print("Could not encode JSON file.\n")

# search()
# def main():
#     country_code = str.lower(input("Enter Country Code: "))
#     lan_code = fetch_lan_code(country_code)
#     print(lan_code)
    
# main()
# my_custom_function()
# try: 
#     with open("data.json", "r") as json_file:
#         existing_data = json.load(json_file)
#         top_news = []
#         for category in existing_data.get("top_news", [])[:1]:
#             for news in category.get("news", [])[:10]:
#                 top_news.append(
#                     {
#                         "Title": news['title'],
#                         "URL": news['url'],
#                         "Publish_Date": news["publish_date"],
#                         "authors": news.get("authors", [])
#                     }
#                 ) 
#         for num in top_news:
#             print(f'{num}\n')
#             for topic, des in enumerate(top_news):
#                 print(f'{topic}: {des}\n')
#             # print(top_news)
# except (FileNotFoundError, json.decoder.JSONDecodeError):
#     if FileNotFoundError:
#         print("File not found.\n")

#     else:
#         print("Could not encode JSON file.\n")

# try:
#     with open("country_code.json", 'r') as codes:
#         data = json.load(codes)
#         for country, code in data.items():
#             print(f"{country} : {code}")
    
# except (FileNotFoundError, json.decoder.JSONDecodeError):
#     if FileNotFoundError:
#         print("File not found.\n")

#     else:
#         print("Could not encode JSON file.\n")