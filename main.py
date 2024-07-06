import os
from dotenv import load_dotenv, find_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import  ApplicationBuilder,  CommandHandler, CallbackQueryHandler, CallbackContext, InlineQueryHandler, ContextTypes
from newsAPI import fetch_lan_code, fetch_TopNews, search_news, search_random
import logging
from uuid import uuid4
import json

#Fectching token from the environment
load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")

#logging console to see what is processing or if there're any errors
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

#start commands
async def start(update: Update, context: CallbackContext) -> None:
    # Get user that sent /start and log his name on the console / terminal
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    msg = (
        f"Hello, {update._effective_user.first_name}! 🤖\n\n"
        "I am your local bot that will tell you Top News Around the world. 🌍🗞️\n"
        "Just type /top and choose the country ⭐\n"
        "Use /help to see available commands! \n"
    )
    await update.message.reply_text(msg)

#help command
async def help(update: Update, context: CallbackContext) -> None:
    msg = (
        f"Hello {update._effective_user.first_name}. 🤖\n\n"
        "My Commands are Simple. 🧩\n"
        "**/start** - See what the bot can do! 🗝️\n"
        "**/top** - to check top news around the world. 🗞️\n"
        "**/search <TOPIC>** - Search the news related to Topic; Replace **TOPIC** with the name of the TOPIC without <>.🎏 \n"
        "That's not all. There's a cool feature. 😉⌚\n"
        "Type `@timmy_news_bot` **<TOPIC>** \n"
        "It'll fetch you a random news related to the Topic. 🤓\n"
    )
    await update.message.reply_text(msg, parse_mode = 'Markdown')

#fectch available country for top news.
async def country(update: Update, context: CallbackContext) -> None:
    try:
        with open("country_code.json", 'r') as codes:
            data = json.load(codes)
        
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        if FileNotFoundError:
            print("File not found.\n")

        else:
            print("Could not encode JSON file.\n")

    keyboard = [
            InlineKeyboardButton(country, callback_data=str(country_code))
            for country, country_code in data.items()
        ]
    layout = [keyboard[i:i + 4] for i in range(0, len(keyboard), 4)] 
    
    reply_markup = InlineKeyboardMarkup(layout)
    await update.message.reply_text(
        text="Which news from Country Do you want to know? 🗞️🌍\n Select One Option", reply_markup=reply_markup
    )

#Display top news retrieved according to the country
async def top_news(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    country_code = query.data
    await query.answer()
    lan_code = fetch_lan_code(country_code)
    news = fetch_TopNews(country_code, lan_code)
    
    if news:
        msg = "Here's today top stories for the country you chose! 🗞️\n"

        await context.bot.send_message(
            chat_id = query.message.chat_id,
            text = msg,
            parse_mode = "Markdown"
        )
        for new in news:
            news_msg = (
                f" {new['Title']} \n\n"
                f"🔗[Link]({new['URL']})\n\n"
                f"Published Date: __{new['Publish_date']}__\n"
                f"Author: {new['Author'] if new['Author'] else '-'}\n"
            )
            await context.bot.send_message(
                chat_id = query.message.chat_id,
                text = news_msg,
                parse_mode = "Markdown"
            )
    else:
        await query.edit_message_text(text = "It seems that there is someting worong on my side fetching news. 🤖😓\n")

#search function to search new topics         
async def search(update: Update, context: CallbackContext) -> None:
    if context.args:
        new_topic = "+".join(context.args)
        news = search_news(new_topic)
        if news:
            msg = f"Here's the news about {new_topic}.\n"
            await context.bot.send_message(
            chat_id = update.message.chat_id,
            text = msg,
            parse_mode = "Markdown"
        )
            for new in news:
                news_msg = (
                    f" **__{new['Title']}__** \n\n"
                f"🔗[Link]({new['URL']})\n\n"
                f"Published Date: __{new['Publish_date']}__\n"
                f"Author: {new['Author'] if new['Author'] else '-'}\n"
                )
                print(news_msg)

                await context.bot.send_message(
                    chat_id = update.message.chat_id,
                    text = news_msg,
                    parse_mode = "Markdown"
                )
        else:
            await update.message.reply_text(text = "It seems that there is someting worong on my side fetching news. 🤖😓\n")

    else:
        await update.message.reply_text(text = "You need to provide me with a topic to search it up.\n Usage: \search TOPIC\n")

#fetch a random new according to the topic provided   
async def random(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.inline_query.query
    if query:
        topic = query.replace(" ", "+")
        news = search_random(topic)
        random_new = news[0]
        new_msg = (
                    f" {random_new['Title']} \n\n"
                f"🔗[Link]({random_new['URL']})\n\n"
                f"Published Date: __{random_new['Publish_date']}__\n"
                f"Author: {random_new['Author'] if random_new['Author'] else '-'}\n"
                )

        if topic:
            results = [
            InlineQueryResultArticle(
                id = str(uuid4()),
                title = f"Search {topic}",
                input_message_content=InputTextMessageContent(new_msg)
                
            )
        ]
            await update.inline_query.answer(results)

        else:
            await query.edit_message_text(text = "It seems that there is someting worong on my side fetching news. 🤖😓\n")

    else:
        return

#main function    
def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("top", country))
    application.add_handler(CommandHandler("search", search))
    application.add_handler(InlineQueryHandler(random))
    application.add_handler(CallbackQueryHandler(top_news))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
