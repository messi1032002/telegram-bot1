import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

TOKEN = "7842334275:AAEa1NE1nMkh7TwwA6GbXQFichhvkWnn1_0"
ADMIN_ID = 1895570058  # Apna Telegram ID dal (check `getUpdates` se)

# Load Users List
def load_users():
    try:
        with open("users.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save Users List
def save_users(users):
    with open("users.json", "w") as file:
        json.dump(users, file)

# Start Command: Jab Koi Bot Start Kare
async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    users = load_users()

    if user.id not in users:
        users.append(user.id)
        save_users(users)
        print(f"✅ New user added: {user.id}")

    await update.message.reply_text(f"👋 Welcome {user.first_name}! You are now connected to the bot.")

# Function to Send Messages Instead of Forwarding
async def send_to_all(update: Update, context):
    if update.message and update.message.from_user.id == ADMIN_ID:
        users = load_users()
        message_text = update.message.text  # Message Text
        if not message_text:
            return

        for user_id in users:
            try:
                await context.bot.send_message(chat_id=user_id, text=message_text)
                print(f"✅ Sent to {user_id}")
            except Exception as e:
                print(f"❌ Error sending to {user_id}: {e}")

# Bot Setup
def main():
    app = Application.builder().token(TOKEN).build()
    
    # Commands and Message Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_to_all))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()


TOKEN = "7842334275:AAEa1NE1nMkh7TwwA6GbXQFichhvkWnn1_0"
ADMIN_ID = 1895570058
