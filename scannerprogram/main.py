import requests
import json
import sys
import hashlib

APIKEY = "aca0515a2b6b47ada82b13dca40ee51e"
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
    return format(sha1.hexdigest())


def hash_lookup(hash):
    url = "https://api.metadefender.com/v4/hash/" + hash
    # print("This is the url: " + url)
    headers = {"apikey": APIKEY}
    response = requests.request("GET", url, headers=headers)
    # print(response.status_code)
    # we can get the boolean to see if it was found or not
    # return boolean
    # json_response = json.loads(response.text)
    return response.status_code


# if the results are not found, upload the file and receive a data_id
def upload_file(filepath, filename):
    url = "https://api.metadefender.com/v4/file"
    headers = {
        "apikey": APIKEY,
        "Content-Type": "multipart/form-data",
        "filename": filename
    }
    payload = filepath
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    # get the data_id


# repeated pull result until percentage is 100
def pull_result(data_id):
    url = "https://api.metadefender.com/v4/file/" + data_id
    headers = {
        "apikey": APIKEY,
        "x-file-metadata": ""
    }
    response = requests.request("GET", url, headers=headers)
    json_response = json.loads(response.text)
    print(json_response)

    progress = json_response["scan_results"]["progress_percentage"]
    if progress == "100":
        display_result(json_response["scan_results"])


def display_result(scan_results):
    print("filename: samplefile.txt"
          "overall_status: Clean")
    print("engine: Ahnlab & Cyren"
          "threat_found: SomeBadMalwareWeFound"
          "scan_result: 1"
          "def_time: 2017-12-05T13:54:00.000Z")

def demo():
    url = "https://api.metadefender.com/v4/apikey/"
    headers = {"apikey": APIKEY}
    response = requests.request("GET", url, headers=headers)
    # parse response:
    y = json.loads(response.text)
    # the result is a Python dictionary:
    print(y['max_file_download'])


if __name__ == '__main__':
    # demo()
    filepath = "/Users/leticiasiqueira/Downloads/leticiasiqueiracv.pdf"
    hash_value = hash_calculation(filepath)
    code = hash_lookup(hash_value)
    print(code)
    # command line arguments
    print(sys.argv)
