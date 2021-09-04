import time
import logging
import telepot
from telepot.loop import MessageLoop
from .config import config
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
loop=MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')
logging.basicConfig(filename='debug.log', filemode='w', format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p')
logging.debug(loop)
# Keep the program running.
while 1:
    time.sleep(10)