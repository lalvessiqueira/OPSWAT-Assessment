import requests
import json
import sys
import hashlib

APIKEY = sys.argv[1]


def api_check():
    url = "https://api.metadefender.com/v4/apikey/"
    headers = {
        "apikey": APIKEY
    }
    response = requests.request("GET", url, headers=headers)
    json_response = json.loads(response.text)
    if response.status_code != 200:
        sys.exit(json_response["error"]["messages"])


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


# this response will be checked in file_scanner
def hash_lookup(hash):
    url = "https://api.metadefender.com/v4/hash/" + hash
    # print("This is the url: " + url)
    headers = {"apikey": APIKEY}
    response = requests.request("GET", url, headers=headers)
    # print(response.status_code)
    # json_response = json.loads(response.text)
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
    json_response = json.loads(response.text)
    # print(response.text)
    if response.status_code == 200:
        # print("file uploaded successfully")
        return json_response["data_id"]
    elif response.status_code == 400:
        sys.exit(json_response["error"]["messages"])
    else:
        sys.exit("Status code:" + str(response.status_code))


# repeatedly pull result until percentage is 100
def pull_result(data_id):
    url = "https://api.metadefender.com/v4/file/" + data_id
    headers = {
        "apikey": APIKEY,
        "x-file-metadata": ""
    }
    response = requests.request("GET", url, headers=headers)
    json_response = json.loads(response.text)
    if response.status_code == 200:
        return json_response
    elif response.status_code == 404:
        sys.exit(json_response["error"]["messages"])
    else:
        sys.exit("Status code:" + str(response.status_code))


# send in the json_response
def check_results(data_id):
    json_response = pull_result(data_id)
    # maybe have to change 100 into integer
    while json_response["scan_results"]["progress_percentage"] != 100:
        # print(json_response["scan_results"]["progress_percentage"])
        json_response = pull_result(data_id)
    # once it is 100, then we can call display results
    display_result(json_response)


def display_result(response):
    print("filename: " + response["file_info"]["display_name"])
    print("overall_status: Clean")
    for engine in response["scan_results"]["scan_details"]:
        print_engines(engine, response)


def print_engines(engine, response):
    print("engine:", engine)
    if response["scan_results"]["scan_details"] != {}:
        threat = response["scan_results"]["scan_details"][engine]["threat_found"]
        print("threat_found:", 'Clean' if threat == '' else threat)
        print("scan_result:", response["scan_results"]["scan_details"][engine]["scan_result_i"])
        print("def_time:", response["scan_results"]["scan_details"][engine]["def_time"])
    else:
        sys.exit("No scan details for this file")


def file_scanner(file):
    # 1. Calculate the hash of a given file (i.e. samplefile.txt)
    hash_value = hash_calculation(file)

    # 2. Perform a hash lookup against metadefender.opswat.com and see if
    # there are previously cached results for the file
    hash_response = hash_lookup(hash_value)

    # 3. If results are found, skip to step 6
    if hash_response.status_code == 200:
        # 6. Display results in format below (SAMPLE OUTPUT)
        hash_lookup_json = json.loads(hash_response.text)
        display_result(hash_lookup_json)

    # 4. If results are not found
    elif hash_response.status_code == 404:
        # 4.1 Upload the file and receive a "data_id"
        data_id = upload_file(file)
        # 5. Repeatedly pull on the "data_id" to retrieve results
        check_results(data_id)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("run: python filescanner.py [API_KEY]")

    # check if API_KEY exists
    api_check()

    user_input = input()
    commands = user_input.split(" ")
    if len(commands) != 2 or commands[0] != "upload_file":
        sys.exit("input: upload_file [filename_to_scan]")

    file_scanner(commands[1])
