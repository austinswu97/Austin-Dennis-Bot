#https://www.googleapis.com/language/translate/v2?key=AIzaSyCQnPINQYhHMqFzxppTrHKKRI0gcCHltVk&q=bus&source=en&target=ja

import requests
import json

GOOGLE_API_KEY = 'AIzaSyCQnPINQYhHMqFzxppTrHKKRI0gcCHltVk'

def get_translation(text, source_lang="en", target_lang="ja"):

    googleapi_url  = 'https://www.googleapis.com/language/translate/v2?key=' + GOOGLE_API_KEY + '&q=' + text + '&source=' + source_lang + '&target=' + target_lang

    print googleapi_url

    r = requests.get(googleapi_url)

    print r.text                                                                                                                       

    received_json_data = json.loads(r.text)

    print received_json_data
    return received_json_data['data']['translations'][0]['translatedText']


def main():
    # my code here
    trans_txt = get_translation('english', target_lang="es")
    print trans_txt


if __name__ == "__main__":
    main()
