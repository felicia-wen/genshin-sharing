from config import Config
import time
import telepot
from telepot.loop import MessageLoop
from config import config
import getmhy
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    if content_type == 'text':
        if msg['text'] == '/verify':
            print ("verifying.")
            getmhy.run()
TOKEN = config.TG_BOT_TOKEN
bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)