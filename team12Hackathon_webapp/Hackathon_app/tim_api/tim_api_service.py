import os


class TimApiService(object):

    def __init__(self):
        self.api_token = os.environ.get('API_TOKEN_TIM')
        self.api_url = os.environ.get('API_URL_TIM')
        if not self.api_token:
            raise ValueError('Api tim token is empty.')
        if not self.api_url:
            raise ValueError('Api url is empty.')
