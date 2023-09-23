from sqlite3 import connect
import subprocess
from urllib import response
from h11 import Request
import telegram
from telegram import (
    InlineKeyboardMarkup,
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
    WebAppInfo,
    InlineKeyboardButton,
    MenuButton,
    ReplyKeyboardRemove,
    MenuButtonWebApp,
    Bot,
)
from telegram import _bot
import requests
from telegram.ext import (
    ApplicationBuilder,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    Updater,
)
import random

from telegram import Bot
from db import create_tables, insert_feedback, Message, Feedback
import json

# Creds to be stored in the env files
BOT_TOKEN = "6545283229:AAFeAp7BFtT3rg6_GXN88NiPPeHTzjG2Vs4"
BOT_USERNAME = "@feedback_account_bot."


# entry point of the bot
async def start(update, context):
    print("Started")
    contact_button = KeyboardButton("Share Mobile Number", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[contact_button]], resize_keyboard=True)
    response = await context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Please share your mobile number:",
        reply_markup=reply_markup,
    )


# This is the function to trigger the react app
async def handle_contact(update, context):
    # Generate a random number
    random_number = generate_random_number()

    # Check if the number is odd or even
    result = check_odd_even(random_number)
    data = {
        "chat_id": update.message.chat.id,
        "menu_button": {
            "type": "web_app",
            "text": result,
            "web_app": {"url": MY_WEBSITE},
        },
    }
    setmenubutton(data)
    phone_number = update.message.contact.phone_number
    first_name = update.message.contact.first_name
    type = checkType(result)

    kb = [
        [
            InlineKeyboardButton(
                result,
                web_app=WebAppInfo(
                    # f"https://calm-profiterole-ca4923.netlify.app/?mobileNumber={phone_number}&&first_name={first_name}"
                    f"https://feedback-beryl-eight.vercel.app/?mobileNumber={phone_number}&&first_name={first_name}&&button_text={result}&&type={type}"
                ),
            )
        ]
    ]
    response = await update.message.reply_text(
        "Let's do this...", reply_markup=InlineKeyboardMarkup(kb)
    )


def generate_random_number():
    # Generate a random integer between 1 and 100
    random_number = random.randint(1, 100)
    return random_number


# utils functions
def check_odd_even(number):
    if number % 2 == 0:
        return "Give feedback"
    else:
        return "Fill account details"


def setMyCommands(chat_id, data):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setMyCommands"
    print(url, "url")
    print(chat_id, "chat_id")
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Check for HTTP errors
        print("success")
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None


def deleteMyCommands(chat_id, data):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMyCommands"
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Check for HTTP errors
        print("success")
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None


def setmenubutton(data):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setChatMenuButton"

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=data, headers=headers)
    print(response, "resp")


def error():
    return


def checkType(text):
    if text == "Fill account details":
        return "2"
    else:
        return "1"


application = ApplicationBuilder().token(BOT_TOKEN).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.CONTACT, handle_contact))
# application.add_error_handler(error)

if __name__ == "__main__":
    # when we run the script we want to first create the bot from the token:

    # and send the bot on its way!
    print(
        f"Your bot is listening! Navigate to http://t.me/{BOT_USERNAME} to interact with it!"
    )

    application.run_polling()
