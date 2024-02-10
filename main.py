from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

#Bot variables
TOKEN: Final = "token"
BOT_USERNAME: Final = "@bot"

#Commands
async def start_command(update:Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to this new Bot!!")

async def help_command(update:Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Try the command italy for famous Italian quotes")

async def italy_command(update:Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("If only a little good existed in the world \nand each considered himself the other's brother\nthere would be fewer painful thoughts and fewer pains\nand the world would be much more beautiful")

#Responses

def handle_Response(text: str) -> str:

    processed: str = text.lower()

    if 'hello' in processed:
        return "hey"
    
    if "best anime character?" in processed:
        return "Obv Juuzou or Jiraiya"
    
    if "test" in processed:
        return "test"
    
    return "Bro, i didn't uderstand"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type #group chat or single chat
    text: str = update.message.text #input message
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response:str = handle_Response(new_text)

        else: return
    else:
        response:str=handle_Response(text)

    print(response)
    await update.message.reply_text(response)

#Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

#MAIN 
if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    #Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("italy", italy_command))

    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Error
    app.add_error_handler(error)

    #Polls the bot
    print("Polling...")
    app.run_polling(poll_interval=3)