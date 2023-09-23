import subprocess
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
from db import create_tables, insert_feedback, Message, Feedback
import json

print()
BOT_TOKEN = "6274194101:AAGLeYbQj88EeD6uQrX7CC3g0SzlPTHFwLw"
BOT_USERNAME = "@farmstack_web_bot."


async def start(update: Update, context: CallbackContext):
    # Handle the /start command
    chat_id = update.message.chat_id

    contact_button = KeyboardButton("Share Mobile Number", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[contact_button]], resize_keyboard=True)

    response = await context.bot.send_message(
        chat_id=chat_id,
        text="Please share your mobile number:",
        reply_markup=reply_markup,
    )
    data = {
        "commands": [],
    }
    send_telegram_message("s", 1, "", data)
    message_id = response.message_id
    context.user_data["message_id"] = message_id


async def launch_web_ui(update: Update, callback: CallbackContext):
    query = update.callback_query

    try:
        print("contact number shared", update)
        # subprocess.run("pbcopy", text=True, input="copied")

        phone_number = ""
        first_name = ""
        if update.message.contact:
            phone_number = update.message.contact.phone_number
            first_name = update.message.contact.first_name
            button_text = checkAndReturn(phone_number)
            type = checkType(button_text)
            data = {
                "commands": [
                    {"command": "feedback", "description": "scome"},
                    {"command": "account", "description": "As"},
                ],
            }
            send_telegram_message("s", 1, "", data)
            # async set_chat_menu_button()
            # reply_markup = MenuButtonWebApp(
            #     text="web_app",
            #     web_app=WebAppInfo(
            #         f"https://feedback-beryl-eight.vercel.app/?mobileNumber=phone_number&&first_name=first_name&&button_text=button_text&&type=type"
            #     ),
            # )
            # _bot.set_chat_menu_button()

            # await update.message.reply_text(
            #     "Click the button to open the web app:",
            #     reply_markup=MenuButton(web_app_data=MenuButtonWebApp),
            # )
            # InlineKeyboardButton()
            # kb= [MenuButton( web_app=WebAppInfo(
            #                 # f"https://calm-profiterole-ca4923.netlify.app/?mobileNumber={phone_number}&&first_name={first_name}"
            #                 f"https://feedback-beryl-eight.vercel.app/?mobileNumber={phone_number}&&first_name={first_name}&&button_text={button_text}&&type={type}"
            #             )]

            # kb = [
            #     [
            #         InlineKeyboardButton(
            #             button_text,
            #             web_app=WebAppInfo(
            #                 # f"https://calm-profiterole-ca4923.netlify.app/?mobileNumber={phone_number}&&first_name={first_name}"
            #                 f"https://feedback-beryl-eight.vercel.app/?mobileNumber={phone_number}&&first_name={first_name}&&button_text={button_text}&&type={type}"
            #             ),
            #         )
            #     ]
            # ]

            # response = await update.message.reply_text(
            #     "Let's do this...", reply_markup=InlineKeyboardMarkup(kb)
            # )
            # print("REPONSE", response)

        else:
            print("web app replied", update)

            reply_markup = ReplyKeyboardRemove()

            data = json.loads(update.message.web_app_data.data)
            print(update, "data phone")
            #  {'name': 'asdfgbn', 'email': 'kanhaiyasuthar0@gmail.com', 'rating': 'good', 'description': 'asdfbg'}. Thank you for your feedback!
            insert_feedback(
                data["name"],
                "",
                data["phone_number"],
                data["email"],
                data["description"],
                data["rating"],
            )
            await callback.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Thanks for the feedback!",
                reply_markup=reply_markup,
            )
            await update.message.reply_text(f"Your data was: {data}.")

        # print(update.message.contact)
        # phone_number = "987656789"

    except Exception as ex:
        print(ex, "update something went worng")
        await update.message.reply_text(f"Something went wrong.")


async def web_app_data(update: Update, context: CallbackContext):
    print("saving data")
    data = json.loads(update.message.web_app_data.data)
    print(data, "data")
    await update.message.reply_text(
        f"Your data was: {data}. Thank you for your feedback!"
    )


import random


def checkAndReturn(phone_number):
    if not isinstance(phone_number, str):
        return "Invalid input. Please provide a valid phone number as a string."

    # Remove any non-digit characters from the phone number
    cleaned_phone_number = "".join(filter(str.isdigit, phone_number))

    if len(cleaned_phone_number) == 0:
        return "Invalid phone number. Please provide a valid phone number."

    random_number = random.randint(1, 100)  # Generate a random number between 1 and 100

    if random_number % 2 == 0:
        return "Fill account details"
    else:
        return "Give feedback"


def checkType(text):
    if text == "Fill account details":
        return "2"
    else:
        return "1"


async def open_web_app(update: Update, context: CallbackContext):
    print("INSIDE")
    # Construct the URL of the web app
    web_app_url = "https://your-web-app-url.com"  # Replace with your web app's URL

    # Create an inline keyboard button with the web app URL
    keyboard = [[InlineKeyboardButton("Open Web App", url=web_app_url)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send a message with the inline keyboard button
    await update.message.reply_text(
        "Click the button to open the web app:", reply_markup=reply_markup
    )


def send_telegram_message(chat_id, type, command, data):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setMyCommands"

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Check for HTTP errors
        print("success")
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None


# def setmenubutton(chat_id, type, command, data):
# MY_WEBSITE = "https://www.youtube.com"  # Replace with your actual website URL

# data = {
#     "chat_id": chat_id,
#     "menu_button": {
#         "type": "web_app",
#         "text": "Menu",
#         "web_app": {"url": MY_WEBSITE},
#     },
# }

# url = f"https://api.telegram.org/bot{BOT_TOKEN}/setChatMenuButton"

# headers = {"Content-Type": "application/json"}

# response = requests.post(url, json=data, headers=headers)
# print(response, "resp")


async def feedback(update: Update, callback: CallbackContext):
    # print(update, "update")
    # phone_number = update.message.contact.phone_number
    # print(phone_number, "phone_number")
    # first_name = "update.message.contact.first_name"
    # button_text = checkAndReturn(phone_number)
    # type = checkType(button_text)
    kb = [
        [
            InlineKeyboardButton(
                "button_text",
                web_app=WebAppInfo(
                    # f"https://calm-profiterole-ca4923.netlify.app/?mobileNumber={phone_number}&&first_name={first_name}"
                    f"https://feedback-beryl-eight.vercel.app/?mobileNumber=phone_number&&first_name=first_name&&button_text=button_text&&type=as"
                ),
            )
        ]
    ]
    setmenubutton(1465932798, 1, "command", "data")

    response = await update.message.reply_text(
        "Let's do this...", reply_markup=InlineKeyboardMarkup(kb)
    )


application = ApplicationBuilder().token(BOT_TOKEN).build()
# updater = Updater(BOT_TOKEN, use_context=True)
# dispatcher = updater.dispatcher

# and let's set a command listener for /start to trigger our Web UI
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("openwebapp", open_web_app))
application.add_handler(CommandHandler("feedback", feedback))
application.add_handler(MessageHandler(filters.ALL, launch_web_ui))
# application.add_handler(CommandHandler("feedback", open_web_app))
# application.add_handler(CallbackQueryHandler(start, "start"))
# application.add_handler(CallbackQueryHandler(launch_web_ui, "^done_feedback$"))
# application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))

if __name__ == "__main__":
    # when we run the script we want to first create the bot from the token:

    # and send the bot on its way!
    print(
        f"Your bot is listening! Navigate to http://t.me/{BOT_USERNAME} to interact with it!"
    )
    application.run_polling()
