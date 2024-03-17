from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
import shutil

#Bot variables
TOKEN: Final = "Not gonna tell you the token" #Father bot token
BOT_USERNAME: Final = "@AsdyraBot" #Bot username
users = {} #hashmap to let multiple user use the bot at the same time, the values of the hash map are CLIENT_ID = [FLAG, Custom1 FLAG, Custom2 Flag, TRASPARENT FLAG]
usersColor1 = {} # RGB values of the first custom color CLIENT_ID = [R,G,B]
usersColor2 = {} # RGB values of the second custom color CLIENT_ID = [R,G,B]
#Commands
async def start_command(update:Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to this new Bot able to generate QR Codes!!") #start command message

async def help_command(update:Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a simple Telegram bot that enables you to create QR Codes online, here is the command list:\n"+
                                    "1- /help - Return the list of commands\n"+
                                    "2- /colors - Return the list of implemented colors of the Bot\n"+
                                    "3- /generateQR - The bot will send you the QR Code you need after reading your inputs"+
                                    "4- /custom1 - Sending a message with the R;G;B values you'll be able to choose a custom color and calling custom1 you'll be able to set the background/code color to your custom color"+
                                    "4- /custom2 - Sending a message with the R;G;B values you'll be able to choose a custom color and calling custom2 you'll be able to set the background/code color to your custom color")  

async def colors_command(update:Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You can choose between different colors for the code and the background:\n"+
                                    "\t-Blue\n"+
                                    "\t-Green\n"+
                                    "\t-Red\n"+
                                    "\t-Pink\n"+
                                    "\t-Orange\n"+
                                    "\t-Black\n"+
                                    "\t-White\n"+
                                    "\t-Transparent (only for Background)"+
                                    "You can also write \"custom1\" or \"custom2\" to use the custom color if set, if you don't have set them you can set them with the command \\custom1 and \\custom2")
    
async def generateQR_command(update:Update, context: ContextTypes.DEFAULT_TYPE):
    users[update.message.chat.id] = [True, False, False, False] #setting the flag of the user who wants to create a QR Code to 1
    await update.message.reply_text("Write the link or datas you want to convert followed by the code color and the background color (DATAS, CODE COLOR, BG COLOR) the background color can be trasparent, to have a list of the colors you can use digit \\color \nCopy the following message to make the process faster")
    await update.message.reply_text("QRDATAS, CodeCOlor, BgColor")


async def custom1_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users[update.message.chat.id] = [False, True, False, False]
    await update.message.reply_text("Write the RGB values separeted by a comma (R,G,B), the values must go from 0 to 255\n"+
                                    "You can call the custom color by writing \"custom2\" instead of a color in the command \\gereateQR")

async def custom2_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users[update.message.chat.id] = [False, False, True, False]
    await update.message.reply_text("Write the RGB values separeted by a comma (R,G,B), the values must go from 0 to 255\n"+
                                    "You can call the custom color by writing \"custom2\" instead of a color in the command \\gereateQR")

#Responses
def handle_Response(update: Update,text: str) -> str:
    
    userFlag = users[users.get(update.message.chat.id)]
    out = "Select a command before sending some datas"

    if userFlag[0] == True:
        #handling the input
        data = text.split(',')
        qrDatas = data[0]
        codeColor = data[1]
        bgColor = data[2]
        qrDatas = qrDatas.lower
        codeColor = codeColor.capitalize
        bgColor = bgColor.capitalize
        effCodeColor = colorHandling(update, codeColor) #the effective RGB datas of the code in an array
        effBgColor = colorHandling(update, bgColor) #the effective RGB datas of the background in an array
        
    if userFlag[1] == True:
        #handling the input 
        data = text.split(',')
        R = data[0]
        G = data[1]
        B = data [2]
        usersColor1[users.get(update.message.chat.id)] = [R,G,B]

    if userFlag[2] == True:
        #handling the input 
        data = text.split(',')
        R = data[0]
        G = data[1]
        B = data [2]
        usersColor2[users.get(update.message.chat.id)] = [R,G,B]

def colorHandling(update: Update,color:str): #given the color name returning the RGB Values
    color = color.capitalize

    match color:
        case "Blue":
            return [25, 47, 88, False] #returning the RGB values and the transparent flag
        case "Green":
            return [34, 139, 34, False]
        case "Red":
            return [220, 20, 60, False]
        case "Pink":
            return [255, 182, 193, False]
        case "Orange":
            return [255, 127, 80, False]
        case "Black":
            return [0, 0, 0, False]
        case "White":
            return [255, 255, 255, False]
        case "Transparent":
            return [255, 255, 255, True]
        case "custom1":
            userData = users.get(update.message.chat.id) #getting all the values in the hashmap of the user
            return [usersColor1[0], usersColor1[1], usersColor1[2], False]
        case "Custom2":
            userData = users.get(update.message.chat.id)
            return [usersColor2[0], usersColor2[1], usersColor2[2], False]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type #group chat or single chat
    text: str = update.message.text #input message

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"') #Console debug 

    if not(update.message.chat.id in users): #if the message is the first message of the user I add him to the hashmap and I set the command flag to 0
        users[update.message.chat.id] = [False,False,False,False]
        usersColor1[update.message.chat.id] = [-1,-1,-1]
        usersColor2[update.message.chat.id] = [-1,-1,-1]

    if message_type == 'group': #if the bot is called in a group
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response:str = handle_Response(new_text)

        else: return 
    else: #if it is in private chat 
        response:str=handle_Response(update,text)

    print(response)
    await update.message.reply_text(response)

#QR code generation

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