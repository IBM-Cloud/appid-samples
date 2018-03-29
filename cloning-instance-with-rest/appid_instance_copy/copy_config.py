#!/usr/bin/env python
import requests
import json
import argparse



def get_from_api(path, token):
    headers = {'Authorization': token, 'Accept': 'application/json'}
    url = management_url + src_tenantId + "/config/" +path
    return requests.get(
        url,
        headers=headers);

def put_to_api(path, content, token):
    headers = {'Authorization': token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
    url = management_url + trgt_tenantId + "/config/" + path
    return requests.put(
        url,
        data=content,
        headers=headers);

def get_iam_token():
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}
    data = 'grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=' + apiKey;

    r = requests.post(iam_url + ".bluemix.net/oidc/token", data=data, headers=headers);
    return 'Bearer ' + json.loads(r.text)['access_token'];

def copy(path, token):
    r = get_from_api(path, token)
    debug(r.status_code)
    debug(r.content)
    if 200 <= r.status_code < 300:
        print("success! got " + path + " from source")
    else:
        print("Failed to get " + path + " from source")
    jcontent = r.content

    r = put_to_api(path, jcontent, token)
    debug(r.status_code)
    debug(r.text)
    if 200 <= r.status_code < 300:
        print("success! put to " + path + " at target")
    else:
        print("Failed to put to " + path + " at target")

def copyTemplates(token):
    copy("cloud_directory/templates/" + "USER_VERIFICATION", token)
    copy("cloud_directory/templates/" + "RESET_PASSWORD", token)
    copy("cloud_directory/templates/" + "WELCOME", token)
    copy("cloud_directory/templates/" + "PASSWORD_CHANGED", token)

def copyActions(token):
    copy("cloud_directory/action_url/" + "on_user_verified", token)
    copy("cloud_directory/action_url/" + "on_reset_password", token)

def debug(str):
    if verbose:
        print(str)

def main():
    parser = argparse.ArgumentParser(description='Copy configuration from one App ID instance to another')
    parser.add_argument('source', type=str,
                        help='The App ID instance id (tenantID) source of configuration')

    parser.add_argument('target', type=str,
                        help='The App ID instance id (tenantID) target to configure')

    parser.add_argument('-k', '--apikey', type=str,
                        help='API Key for creating an IAM token with sufficient privileges')

    parser.add_argument('-r', '--region', type=str, default='us-south',
                        help='IBM Cloud region for source instance. It will also be the target region, unless specified otherwise')

    parser.add_argument('-R', '--target_region', type=str,
                        help='IBM Cloud region for source instance, if different then target')

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Run with verbose mode. REST messages content will be displayed')

    args = parser.parse_args()

    global region
    global src_tenantId
    global trgt_tenantId
    global apiKey
    global iam_url
    global management_url
    global verbose

    src_tenantId = args.source
    trgt_tenantId = args.target
    apiKey = args.apikey
    region = args.region
    verbose = args.verbose

    if region == "us-south":
        region = 'ng'

    iam_url = "https://iam." + region
    management_url = "https://appid-management." + region + ".bluemix.net/management/v4/"

    token = get_iam_token()

    copy("idps/facebook", token)
    copy("idps/google", token)
    copy("idps/cloud_directory", token)
    # copy("idps/saml", token)
    #
    copy("tokens", token)
    # copy("redirect_uris", token)
    copy("users_profile", token)
    # copy("ui/theme_color", token)
    # copy("ui/media", token)
    copy("cloud_directory/sender_details", token)

    copyTemplates(token)
    #copyActions(token)



if __name__ == "__main__":
    main()
