import requests
import json
import sys
import hashlib

'''
SAMPLE INPUT COMMAND:
upload_file samplefile.txt
SAMPLE OUTPUT:
filename: samplefile.txt
overall_status: Clean
'''


# 276808942CB3A179B05AC9AA2B0D447A72E70A33
# Calculate the hash of a given file (i.e. samplefile.txt)
def hash_calculation(filename):
    # cite of code: https://www.tutorialspoint.com/How-to-Find-Hash-of-File-using-Python
    BUF_SIZE = 65536
    sha1 = hashlib.sha1()

    with open(filename, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    print("SHA1: {0}".format(sha1.hexdigest()))


def demo():
    url = "https://api.metadefender.com/v4/apikey/"
    headers = {"apikey": "aca0515a2b6b47ada82b13dca40ee51e"}
    response = requests.request("GET", url, headers=headers)
    # parse response:
    y = json.loads(response.text)
    # the result is a Python dictionary:
    print(y['max_file_download'])


if __name__ == '__main__':
    demo()
    hash_calculation("/Users/leticiasiqueira/Downloads/leticiasiqueiracv.pdf")
