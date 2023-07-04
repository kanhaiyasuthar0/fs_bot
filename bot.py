import imp
from telegram import (
    InlineKeyboardMarkup,
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
    WebAppInfo,
    InlineKeyboardButton,
    MenuButton,
)
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
    print("going ahead")

    message_id = response.message_id
    context.user_data["message_id"] = message_id


async def launch_web_ui(update: Update, callback: CallbackContext):
    # For now, let's just acknowledge that we received the command
    # print("sending the option to launch web ui", update)
    query = update.callback_query
    # print("update", update)
    try:
        phone_number = ""
        first_name = ""
        if update.message.contact:
            phone_number = update.message.contact.phone_number
            first_name = update.message.contact.first_name
            kb = [
                [
                    InlineKeyboardButton(
                        "Give the feedback",
                        web_app=WebAppInfo(
                            f"https://calm-profiterole-ca4923.netlify.app/?mobileNumber={phone_number}&&first_name={first_name}"
                        ),
                    )
                ]
            ]
            await update.message.reply_text(
                "Let's do this...", reply_markup=InlineKeyboardMarkup(kb)
            )
        else:
            data = json.loads(update.message.web_app_data.data)
            print(data, "data phone")
            #  {'name': 'asdfgbn', 'email': 'kanhaiyasuthar0@gmail.com', 'rating': 'good', 'description': 'asdfbg'}. Thank you for your feedback!
            insert_feedback(
                data["name"],
                "",
                data["phone_number"],
                data["email"],
                data["description"],
                data["rating"],
            )
            await update.message.reply_text(
                f"Your data was: {data}. Thank you for your feedback!"
            )

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


application = ApplicationBuilder().token(BOT_TOKEN).build()
# updater = Updater(BOT_TOKEN, use_context=True)
# dispatcher = updater.dispatcher

# and let's set a command listener for /start to trigger our Web UI
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.ALL, launch_web_ui))
# application.add_handler(CallbackQueryHandler(launch_web_ui, "^done_feedback$"))
# application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))

if __name__ == "__main__":
    # when we run the script we want to first create the bot from the token:

    # and send the bot on its way!
    print(
        f"Your bot is listening! Navigate to http://t.me/{BOT_USERNAME} to interact with it!"
    )
    application.run_polling()
