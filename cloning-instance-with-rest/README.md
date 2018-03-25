# Cloning an App ID instance example

Here is an example of how to use the App ID management APIs to create a script that can be used to easily copy the configuration of one instance of App ID to another.
The script can be part of the organization DevOps pipeline and specific permissions can be granted just for this task by the IBM Cloud platform. 
We will demonstrate how the script can get an api-key to authenticate with and get the limited IAM credentials that will enable it to access App ID APIs and copy the configuration of an existing App ID instance to a newly created instance.

### Initial steps
1. The App ID service instance to copy configuration from will be referred to as the 'source instance'. In the same IBM Cloud account, create a new instance (either from dashboard or using bx CLI) which will be referred to as the 'target instance'  

2. The owner of the account logs in to IBM Cloud console and creates a new Service ID.  See how [here](https://console.bluemix.net/docs/iam/serviceid.html#serviceids)

2. The owner will create an access policy to the service with the service role of a `Writer` to all App ID services in the account. See how [here](https://console.bluemix.net/docs/iam/serviceidaccess.html#serviceidpolicy)

	You can read more about App ID actions and roles at [this article](https://console.stage1.bluemix.net/docs/services/appid/iam.html#service-access-management)

4. The owner will now create an api-key to this service ID, which he will later pass to the DevOps person that operates the cloning task. See how [here](https://console.bluemix.net/docs/iam/serviceid_keys.html#serviceidapikeys) 
 
For a detailed walkthrough on how to create and manage service IDs see this good [blog](https://www.ibm.com/blogs/bluemix/2017/10/introducing-ibm-cloud-iam-service-ids-api-keys/) post.

> Note: For simplicity, this example shows the cloning of an instance in the same account as the source. For cloning from one account to another, you will be creating 2 different service IDs, one in the source account and another in the target account. Then you will set the policies as appropriate so that the source will have read rights and target will have edit rights, and you will need to use the 2 different api-keys you will create in the cloning script. 

### Installing the cloning script

**Prereq:**  You will need to have [python](https://www.python.org/downloads/) installed. If you are using Mac or Linux, most of the chances you already have it.

1. Get the App ID samples repository from github   
	`git clone https://github.com/IBM-Cloud/appid-samples.git` 
2. Go into the cloning script folder  
	`cd appid-samples/cloning-instance-with-rest`
3. Install the script as a command line script  
  `Sudo python setup.py install`
  
### Executing the cloning script
Now that you have the script installed run the following command in terminal:
`appidc -h`  
This will display the command help as following:  

```
usage: appidc [-h] [-k APIKEY] [-r REGION] [-R TARGET_REGION] [-v VERBOSE]
              source target

Copy configuration from one App ID instance to another

positional arguments:
  source                The App ID instance id (tenantID) source of
                        configuration
  target                The App ID instance id (tenantID) target to configure

optional arguments:
  -h, --help            show this help message and exit
  -k APIKEY, --apikey APIKEY
                        API Key for creating an IAM token with sufficient
                        privileges
  -r REGION, --region REGION
                        IBM Cloud region for source instance. It will also be
                        the target region, unless specified otherwise
  -R TARGET_REGION, --target_region TARGET_REGION
                        IBM Cloud region for source instance, if different
                        then target
  -v VERBOSE, --verbose VERBOSE
                        Run with verbose mode. REST messages content will be
                        displayed
```  

For example, running the command like this: 
`appidc xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx yyyyyyy-yyyy-yyyy-yyyy-yyyyyyyy -k KkKkKkKkkKkKkKkKk -r eu-gb`  
Will copy all configuration from instance with ID xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx to instance with ID yyyyyyy-yyyy-yyyy-yyyy-yyyyyyyy using Service API key KkKkKkKkkKkKkKkKk which are both at the IBM Cloud UK region.

This is it!  
If you are looking for more information about App ID management APIs please refer to our [documentation](https://console.bluemix.net/docs/services/appid/api-reference.html#managing-app-id-with-the-api)
