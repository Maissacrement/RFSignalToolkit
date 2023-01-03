from dotenv import load_dotenv
import requests
import os
import json
from time import sleep

# Load dotenv
load_dotenv()
DEEPL_KEY=os.getenv('DEEPL_KEY')

class Deepl():
    """docstring for Deepl."""

    def __init__(self):
        pass

    def auth(self):
        link = 'https://api-free.deepl.com/v2/usage?auth_key=' + DEEPL_KEY

        return requests.get(link)

    def translate(self, txt, language='fr'):
        postData = {
            'text' : txt, 'auth_key': '16ee3099-d38a-4b50-594b-fce1d74b0132',
            'target_lang': language, 'source_lang': 'zh'
        }

        try:
            response = requests.post(
                'https://api.deepl.com/v2/translate', data=postData
            )

            if response.status_code == 200:
                data = json.loads(response.text)
                return data['translations'][0]['text']

        except Exception as e:
            print('No data fecth', e)

        return txt

# TEST
def main(sentence):
    deeplM = Deepl()
    #print(deeplM.auth().text)
    print(deeplM.translate(str(sentence)))

if __name__ == '__main__':
    import sys
    if(len(sys.argv) > 0 and sys.argv.__contains__('--pipe')):
        while(True):
            main(input())
    elif len(sys.argv) > 1:
        main(sys.argv[1:][0])
