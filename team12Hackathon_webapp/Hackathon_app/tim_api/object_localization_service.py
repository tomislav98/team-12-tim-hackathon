import json
import os
import requests

from Hackathon_app.tim_api.tim_api_service import TimApiService


class ObjectLocalizationService(TimApiService):

    def detect_object(self, base64_file):
        payload = {
                "requests": [
                    {
                        "image": {
                            "content": base64_file
                        },
                        "features": [
                            {
                                "maxResults" : 10,
                                "type": "OBJECT_LOCALIZATION"
                            }

                        ]
                    }
                ]
            }
        headers = {
            'apikey': f'{self.api_token}',
            'Content-Type': 'application/json'
        }
        url = f'{self.api_url}/gcloudvision/v1/images:annotate'
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code != 200:
            print('Cannot detect object')
            return (None, None)
        obj = json.loads(response.text.encode('utf8'))['responses'][0]['localizedObjectAnnotations']
        return (obj['name'], obj['score'])


