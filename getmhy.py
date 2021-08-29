import requests
import msal
import json
from config import config
def run():
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
    UserId="860ea10b-8bea-4d77-a4c6-a1ca357c9129"
    headers={}
    headers['Authorization']='Bearer '+acquire_token()['access_token']
    res=requests.get("https://graph.microsoft.com/v1.0/users/{}/messages?$filter=(from/emailAddress/address) eq 'noreply@email.mihoyo.com'&$select=subject,receivedDateTime,bodyPreview".format(UserId),headers=headers)
    Dict=json.loads(res.text)['value']
    Dict=Dict[len(Dict)-1]
    time=Dict['receivedDateTime']
    subject=Dict['subject']
    bodyPreview=Dict['bodyPreview']
    text=f"Time: {time}\nSubject: {subject}\nbodyPreview:\n{bodyPreview}"
    url = f'https://{config.TG_BOT_API}/bot{config.TG_BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': config.TG_USER_ID,
        'text': text,
        'disable_web_page_preview': True
    }
    requests.get(url,params=data)
    return print("veritfied.")