import os
from telegram.ext import Updater, MessageHandler, Filters
import openai
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Assign the value of TELEGRAM_TOKEN environment variable to telegram_token variable.
telegram_token = os.getenv('TELEGRAM_TOKEN')


def generateEmail(text):
    # Assign the value of OPEN_AI_API_KEY environment variable to open_ai_api_key variable.
    open_ai_api_key = os.getenv('OPEN_AI_API_KEY')
    try:
        # Set the OpenAI API key
        openai.api_key = open_ai_api_key
        # Generate email response using OpenAI's GPT-3 language model
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Here's a kind, polite, and formal email:\n{text}",
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        # Return the generated email
        return response["choices"][0]["text"]
    except Exception as e:
        # Print error message if an error occurs while generating the email
        print("Error generating email:", e)
        # Return an error message
        return "Error generating email. Please try again later."


def handle_message(update, context):
    # Get the user's message from the update
    message = update.message.text
    # Generate an email response using the user's message
    email = generateEmail(message)
    # Set the response to the generated email
    response = email
    # Send the response to the user's chat
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=response)


# Create an Updater object with the Telegram bot token and use_context=True
updater = Updater(
    token=telegram_token, use_context=True)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# Add a MessageHandler to handle text messages (not commands) using handle_message function
dispatcher.add_handler(MessageHandler(
    Filters.text & (~Filters.command), handle_message), group=0)

# Start the bot
updater.start_polling()
