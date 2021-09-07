import requests
import msal
import json
import time
from .config import config
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
    res=requests.get("https://graph.microsoft.com/v1.0/users/{}/messages?$filter=(from/emailAddress/address) eq 'noreply@email.mihoyo.com'&$select=subject,receivedDateTime,bodyPreview".format(config.USER_ID),headers=headers)
    Dict=json.loads(res.text)['value']
    Dict=Dict[len(Dict)-1] #Dict num start from 0,len start from 1.
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
        'disable_web_page_preview': True
    }
    print("Pushing...")
    requests.get(url,params=data)
    return print("Verified.")