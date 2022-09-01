import requests
import json

'''
SAMPLE INPUT COMMAND:
upload_file samplefile.txt
SAMPLE OUTPUT:
filename: samplefile.txt
overall_status: Clean
'''

def demo():
    url = "https://api.metadefender.com/v4/apikey/"
    headers = {
        "apikey": "aca0515a2b6b47ada82b13dca40ee51e"
    }
    response = requests.request("GET", url, headers=headers)
    # parse response:
    y = json.loads(response.text)
    # the result is a Python dictionary:
    print(y['max_file_download'])


if __name__ == '__main__':
    demo()