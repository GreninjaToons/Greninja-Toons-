import os
import telebot
from flask import Flask, request

# Initialize Flask app
app = Flask(__name__)

# Initialize Telebot with your API key
bot = telebot.TeleBot("6707834673:AAGcTUt1a8iWWHuNJAwvF5zRtfI3VFkNue4")

# Define the function to handle messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Check if the message contains a URL
    if message.entities and message.entities[0].type == 'url':
        url = message.text
        # Check if the URL contains a token parameter
        if 'token=' in url:
            # Extract the token from the URL
            token = url.split('token=')[1].split('&')[0]
            # Construct the new URL format
            new_url = f"https://atglinks.com/{token}"
            bot.reply_to(message, f"Converted URL: {new_url}")
        else:
            bot.reply_to(message, "The provided URL does not contain a token parameter.")
    else:
        bot.reply_to(message, "Please provide a valid URL.")

# Define a route for the webhook
@app.route('/' + os.getenv('token'), methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

# Define a route for setting the webhook
@app.route("/set_webhook", methods=['GET', 'POST'])
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://your-app-url/' + os.getenv('token'))
    return "Webhook was set", 200

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
