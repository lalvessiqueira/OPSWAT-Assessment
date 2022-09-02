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
    # print("SHA1: {0}".format(sha1.hexdigest()))
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
    # print(response.status_code)
    return response


# if the results are not found, upload the file and receive a data_id
def upload_file(filepath):
    url = "https://api.metadefender.com/v4/file"
    payload = {}
    files = [('someFile', (filepath, open(filepath, 'rb')))]
    headers = {
        'apikey': APIKEY
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)
    if response.status_code == 200:
        print("file uploaded successfully")
        json_response = json.loads(response.text)
        return json_response["data_id"]
    else:
        sys.exit("ERROR: " + str(response.status_code) + " STATUS")
    # get the data_id


# repeatedly pull result until percentage is 100
def pull_result(data_id):
    url = "https://api.metadefender.com/v4/file/" + data_id
    headers = {
        "apikey": APIKEY,
        "x-file-metadata": ""
    }
    response = requests.request("GET", url, headers=headers)
    json_response = json.loads(response.text)
    return json_response


# send in the json_response
def check_results(data_id):
    progress = pull_result(data_id)
    # maybe have to change 100 into integer
    while progress["scan_results"]["progress_percentage"] != 100:
        progress = pull_result(data_id)
    # once it is 100, then we can call display results
    display_result(progress["scan_results"])


'''
Check for the file badge
If the hash was scanned by MetaDefender Cloud and there was no 
threat detected, the 'No threat detected' badge will be 
returned (see a preview below in the 'Response Body' section). 
If the hash was detected as infected, the 'Threat detected' 
badge will be returned. If the hash was never scanned by MetaDefender 
Cloud, the 'No information available' badge is displayed.
'''


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


def file_scanner(file):
    # 1. Calculate the hash of a given file (i.e. samplefile.txt)
    hash_value = hash_calculation(file)

    # 2. Perform a hash lookup against metadefender.opswat.com and see if
    # there are previously cached results for the file
    hash_response = hash_lookup(hash_value)

    # 3. If results are found, skip to step 6
    if hash_response.status_code == 200:
        # 6. Display results in format below (SAMPLE OUTPUT)
        print('Success!')
        hash_lookup_json = json.loads(hash_response.text)
        display_result(hash_lookup_json["scan_results"])

    # 4. If results are not found
    elif hash_response.status_code == 404:
        # 4.1 Upload the file and receive a "data_id"
        data_id = upload_file(file)
        # 5. Repeatedly pull on the "data_id" to retrieve results
        check_results(data_id)


if __name__ == '__main__':
    # demo()
    # filepath = "/Users/leticiasiqueira/Downloads/leticiasiqueiracv.pdf"
    # code = hash_lookup(hash_value)
    # print(code)
    # command line arguments
    # print(sys.argv)
    file = sys.argv[1]
    file_scanner(file)
