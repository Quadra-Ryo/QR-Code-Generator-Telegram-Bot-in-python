from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

#Bot variables
TOKEN: Final = "Not gonna tell you the token" #Father bot token
BOT_USERNAME: Final = "@AsdyraBot" #Bot username
users = {} #hasmap to let multiple user use the bot at the same time

#Commands
async def start_command(update:Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to this new Bot able to generate QR Codes!!") #start command message

async def help_command(update:Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a simple Telegram bot that enables you to create QR Codes online, here is the command list:\n"+
                                    "1- /colors - Return the list of implemented colors of the Bot\n"+
                                    "2- /generateQR - The bot will send you the QR Code you need after reading your inputs") 

async def colors_command(update:Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You can choose between different colors for the code and the background:\n"+
                                    "\t-Blue\n"+
                                    "\t-Green\n"+
                                    "\t-Red\n"+
                                    "\t-Pink\n"+
                                    "\t-Orange\n"+
                                    "\t-Black\n"+
                                    "\t-White\n"+
                                    "\t-Transparent (only for Background)\n"+
                                    "You can also")
    
async def generateQR_command(update:Update, context: ContextTypes.DEFAULT_TYPE):
    users[update.message.chat.id] = 1 #setting the flag of the user who wants to create a QR Code to 1
    await update.message.reply_text("Write the link or datas you want to convert followed by the code color and the background color (DATAS, CODE COLOR, BG COLOR)\nCopy the following message to make the process faster")
    await update.message.reply_text("http://,Black,Transparent")

#Responses
def handle_Response(update: Update,text: str) -> str:

    if users.get(update.message.chat.id) == 1:
        #handling the input
        data = text.split(',')
        qrDatas = data[0]
        codeColor = data[1]
        bgColor = data[2]
        qrDatas = qrDatas.lower
        codeColor = codeColor.capitalize
        bgColor = bgColor.capitalize

def colorHandling(color:str): #given the color name returning the RGB Values
    match color:
        case "Blue":
            return [25, 47, 88, "false"]
        case "Green":
            return [34, 139, 34, "false"]
        case "Red":
            return [220, 20, 60, "false"]
        case "Pink":
            return [255, 182, 193, "false"]
        case "Orange":
            return [255, 127, 80, "false"]
        case "Black":
            return [0, 0, 0, "false"]
        case "White":
            return [255, 255, 255, "false"]
        case"Transparent":
            return [255, 255, 255, "true"]
        
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type #group chat or single chat
    text: str = update.message.text #input message

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"') #Console debug 

    if not(update.message.chat.id in users): #if the message is the first message of the user I add him to the hashmap and I set the command flag to 0
        users[update.message.chat.id] = 0
    
    if message_type == 'group': #if the bot is called in a group
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response:str = handle_Response(new_text)

        else: return 
    else: #if it is in private chat 
        response:str=handle_Response(update,text)

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
    app.add_handler(CommandHandler("start", start_command)) #association between the Telegram command start and the function "start_command"
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("color", colors_command))
    app.add_handler(CommandHandler("generateQR", generateQR_command))

    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Error
    app.add_error_handler(error)

    #Polls the bot
    print("Polling...") #Console debug
    app.run_polling(poll_interval=1) #Polling messages requests every second