# from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
# from telegram.ext import (
#     Updater,
#     CommandHandler,
#     MessageHandler,
#     filters,
#     ConversationHandler,
#     CallbackContext,
# )

# CONTACT, FEEDBACK = range(2)


# def start(update: Update, context: CallbackContext):
#     reply_keyboard = [["Share Contact"]]
#     update.message.reply_text(
#         "Please share your contact number:",
#         reply_markup=ReplyKeyboardMarkup(
#             reply_keyboard, one_time_keyboard=True, resize_keyboard=True
#         ),
#     )
#     return CONTACT


# def collect_contact(update: Update, context: CallbackContext):
#     contact = update.message.contact.phone_number
#     update.message.reply_text(
#         f"Thank you for sharing your contact number: {contact}\n\n"
#         "Please provide your feedback using this link: [Feedback Form](https://example.com)",
#         reply_markup=ReplyKeyboardRemove(),
#         parse_mode="MarkdownV2",
#     )
#     return FEEDBACK


# def collect_feedback(update: Update, context: CallbackContext):
#     feedback = update.message.text
#     # Process the feedback here
#     update.message.reply_text("Thank you for your feedback!")
#     return ConversationHandler.END


# BOT_TOKEN = "6274194101:AAGLeYbQj88EeD6uQrX7CC3g0SzlPTHFwLw"
# BOT_USERNAME = "@farmstack_web_bot."


# def main():
#     updater = Updater(BOT_TOKEN)
#     dispatcher = updater.dispatcher

#     conv_handler = ConversationHandler(
#         entry_points=[CommandHandler("start", start)],
#         states={
#             CONTACT: [MessageHandler(filters.ALL.contact, collect_contact)],
#             FEEDBACK: [MessageHandler(filters.ALL.text, collect_feedback)],
#         },
#         fallbacks=[CommandHandler("cancel", cancel)],
#     )

#     dispatcher.add_handler(conv_handler)

#     updater.start_polling()
#     updater.idle()


# if __name__ == "__main__":
#     main()
