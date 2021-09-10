import time
import logging
import telepot
from telepot.loop import MessageLoop
from .config import config
import requests
import msal
import json

#Check
def Run():
    def acquire_token():
        """
        Acquire token via MSAL
        """
        authority_url = 'https://login.microsoftonline.com/'+config.TENANT_ID
        app = msal.ConfidentialClientApplication(
            client_id=config.CLIENT_ID,
            authority=authority_url,
            client_credential=config.CLIENT_SECRET
        )
        token = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
        return token
    headers={}
    headers['Authorization']='Bearer '+acquire_token()['access_token']
    res=requests.get("https://graph.microsoft.com/v1.0/users/{}/messages?$search=MiHoYo&$select=subject,receivedDateTime,bodyPreview".format(config.USER_ID),headers=headers)
    Dict=json.loads(res.text)['value'][0] #First value.
    print (Dict)
    #Dict=Dict[len(Dict)-1] #Dict num start from 0,len start from 1.
    dtime=Dict['receivedDateTime']
    timetuple=time.strptime(dtime, '%Y-%m-%dT%H:%M:%SZ')
    print(timetuple)
    tstamp=time.mktime(timetuple) #Convert to time stamp.
    subject=Dict['subject']
    bodyPreview=Dict['bodyPreview']
    text=f"Time: {time.asctime(timetuple)}\nSubject:\n{subject}\nBodyPreview:\n{bodyPreview}"
    if int(time.mktime(time.gmtime())) - int(tstamp) >= 600:
        text="No new verify requests in 10 min."
        print("No new messages in 10 min.")
    url = f'https://{config.TG_BOT_API}/bot{config.TG_BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': config.TG_USER_ID,
        'text': text,
        'reply_to_message_id': msgid,
        'disable_web_page_preview': True
    }
    print("Pushing...")
    requests.get(url,params=data,timeout=15)
    return print("Verified.")

#Push
msgid=""
def handle(msg):
    global msgid
    content_type, chat_type, chat_id ,chat_date,msgid= telepot.glance(msg,long=True)
    print(content_type, chat_type, chat_id,chat_date,msgid)
    if content_type == 'text':
        if msg['text'] == '/verify'or msg['text'] == '/verify@Paimonisnotbot':
            print ("verifying.")
            logging.debug(Run())
TOKEN = config.TG_BOT_TOKEN
bot = telepot.Bot(TOKEN)
loop=MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')
logging.basicConfig(filename='debug.log', filemode='w', format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p')
logging.debug(loop)

# Keep the program running.
while 1:
    time.sleep(10)