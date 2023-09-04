import os
from keep_me import keep_alive
from Downloader import YTdownload
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import validators



# secrets stored by replit
token = os.environ['TOKEN']
bot_username = os.environ['BOTUSERNAME']
description = os.environ['DESCRIPTION']



# checks if the message is a youtube link
def is_yt_link(message):
   
  for link in message.split():
      
    if validators.url(link):
      return link

  
  return False


# used for downloading (from yt), uploading (to telegram) and eventually deleting the video 
async def send(url, chat_id): 
  
  video = YTdownload(is_yt_link(text), chat_id)
  
  video.download()
  await update.message.reply_text(video.properties)

  music = open(video.filename, 'rb')
  await bot.send_audio(chat_id=chat_id, audio=music)

  video.delete()
  

# there is only one command...it sends the bot desciption, which is a simple guide
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(description)


# Response to message
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text

    print(f'user {update.message.chat.id} in {message_type}: "{text}')

    if message_type == 'group':

        if bot_username in text:
            new_text = text.replace(bot_username, '').strip()
          
            if is_yt_link(text):
              video = YTdownload(str(text), update.message.chat.id)
      
              video.download()
              await update.message.reply_text(str(video.properties()))

              music = open(f'{update.message.chat.id}.mp3', 'rb')
              print(str(video.title))
              await context.bot.send_audio(str(update.message.chat.id),
                                           audio=music,
                                           title= str(video.title),
                                           thumbnail = video.save_thumbnail())
              video.delete()

            else:
              await update.message.reply_text('oopsi woopsie, input a youtube link')

        else:
            return
          
    elif message_type == 'private':
    
      if is_yt_link(text):
  
        video = YTdownload(str(text), update.message.chat.id)
      
        video.download()
        await update.message.reply_text(str(video.properties()))

        music = open(f'{update.message.chat.id}.mp3', 'rb')
        await context.bot.send_audio(str(update.message.chat.id),
                                     audio = music,
                                     title = str(video.title),
                                     thumbnail = video.save_thumbnail())

        video.delete()

      else:
        await update.message.reply_text('oopsi woopsie, input a youtube link')

        
      
      

# error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'update {update} caused error {context.error}')



if __name__ == '__main__':

    print('starting...')
    app = Application.builder().token(token).build()

    # commands
    app.add_handler(CommandHandler('start', start_command))

    # messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # error
    app.add_error_handler(error)

    # polls the bot
    print('polling')
    app.run_polling(poll_interval=3)


keep_alive()
