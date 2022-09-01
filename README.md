# OPSWAT

Generate a simple program to scan a file against our metadefender.opswat.com API.
OPSWAT online product documentation contains details of our publicly available
API along with sample code that shows how to scan a file.
Since it is costly to multi-scan a file, we would like you to implement a hash
lookup prior to deciding to upload a file, then retrieve results and display
them.
Please read through the documentation and sample code found at
https://docs.opswat.com/mdcloud/integrations/public-apis &
https://docs.opswat.com/mdcloud/metadefender-cloud-api-v4/ref to perform the
following logic:
1. Calculate the hash of a given file (i.e. samplefile.txt)
2. Perform a hash lookup against metadefender.opswat.com and see if there are
previously cached results for the file
3. If results are found, skip to step 6
4. If results are not found, upload the file and receive a "data_id"
5. Repeatedly pull on the "data_id" to retrieve results
6. Display results in format below (SAMPLE OUTPUT)
7. You should also have some basic error handling for common HTTP results
It is not necessary to account for every idiosyncrocy of the API.
You can show any errors to the standard error and exit the application.

SAMPLE INPUT COMMAND:

    upload_file samplefile.txt
  
SAMPLE OUTPUT:

    filename: samplefile.txt
  
    overall_status: Clean
  
    engine: Ahnlab
  
    threat_found: SomeBadMalwareWeFound
  
    scan_result: 1
  
    def_time: 2017-12-05T13:54:00.000Z
  
    engine: Cyren
  
    threat_found: Clean
  
    scan_result: 0
  
    def_time: 2017-12-05T17:43:00.000Z
  
    <repeats for each engine>
  

What you will need/helpful hints
=================================================================================
You will need to register for a free account at portal.opswat.com.
This will create an account and generate a trial apikey for
metadefender.opswat.com.
The apikey should be displayed in the Dashboard section under MetaDefender Cloud
once you login to your portal account.
Please note this apikey has rate limiting which you may encounter, this is
normal.
Pay particular attention to the following
- https://docs.opswat.com/mdcloud/integrations/api-authentication-mechanisms

- https://docs.opswat.com/mdcloud/metadefender-cloud-api-v4/ref#tag-file-scanning

- https://docs.opswat.com/mdcloud/metadefender-cloud-api-v4/ref#file-lookupbydataid

- https://docs.opswat.com/mdcloud/metadefender-cloud-api-v4/ref#hash-lookup

What we are looking to see
=================================================================================
Smart component choices, we don't expect you to write a JSON parser or reinvent
an HTTP client.
Clean and well documented code.
Any language choice is fine but should be something easily installed and
evaluated.
A publicly available GIT repo that should contain all your code minus your
apikey, we will be providing our own key when we test it out ourselves.
A cleanly written and descriptive README that instructs us how to build and
execute your project.
We will be testing your project on a clean Ubuntu 20.04 VM or latest Visual
Studio 2022 Windows machine.
You can use whatever language or 3rd party library you want, but it should build
and execute out of the box on the VM, so test accordingly.
