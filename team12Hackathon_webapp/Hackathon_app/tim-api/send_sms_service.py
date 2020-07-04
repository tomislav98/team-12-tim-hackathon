import os
import requests

class SendSmsService:

    def __init__(self):
        self.api_token = os.environ.get('API_TOKEN_TIM')
        self.api_url = os.environ.get('API_URL_TIM')
        if not self.api_token:
            raise ValueError('Api tim token is empty.')
        if not self.api_url:
            raise ValueError('Api url is empty.')

    def send_sms(self, phone_number, content):
        if not content:
            print('Not going to send message cause has empty content')
            return False
        if not phone_number:
            print('Not going to send message cause has empty phone number')
            return False
        url = f"{self.api_url}/sms/mt"
        headers = {
            'apikey': f'{self.api_token}',
            'Content-Type': 'application/json'
        }
        payload = "{\n    \"address\": \"tel:+39"+ phone_number +"\",\n    \"message\": \""+ content +" \"\n}"
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            return True
        print(f'response status code : {response.content}')
        return False

