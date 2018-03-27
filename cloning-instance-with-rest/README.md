# Cloning an App ID instance

With App ID, you can now manage your service instance with an API!

Cool, right? 

But even better than that, you can use the management API to create a script that copies an instance configuration from one service instance to another. This means that you don't have to assign service access roles in each instance, you can do the work once, and then replicate it. You can integrate this script as part of your DevOps pipeline.

But, how do I do that while making sure I'm still giving the right people, the right access?

Glad you asked.

In this blog, we will walk you through using a script to obtain an API-key, and limited IAM credentials that you can use to access the App ID APIs. 

## Prerequisites

* You must be the owner of your IBM Cloud account.
* [Python](https://www.python.org/downloads/) must be installed. If you are working on a Mac or Linux machine, you may already have it installed. If not, you can use the provided link.
* An App ID service instance that you have configured with the appropriate levels of access. From now on, we'll refer to this instance as the source instance.
* A second App ID service instance in the same account. Going forward, this instance will be known as the target instance. 


### Obtaining a service ID and API-key

1. As an account owner, log into the IBM Cloud console and [create a new service ID](https://console.bluemix.net/docs/iam/serviceid.html#serviceids). Navigate to **Manage > Security > Identity and Access** and then select **Service IDs**. For a detailed walkthrough of creating and managing service IDs, check out [this blog](https://www.ibm.com/blogs/bluemix/2017/10/introducing-ibm-cloud-iam-service-ids-api-keys/).

2. Create an API-key for the service ID that you created previously. You'll need to pass this key to the DevOps person who operates the cloning task.

		>Tip: For simplicity, this example shows how to clone an instance in the same account as the source. To clone to another account, you can create 2 service IDs and API-keys; one in your source account and the other in your target account. 


## Assigning access policies

2. Create an access policy in the source instance by assigning the service ID the service role of `Reader`.

		>Tip: Be sure that you only give the service ID the rights to complete the tasks that you want it to. If you give too much, the ID has the ability to affect more than you intend. To learn more about App ID actions and roles, check out our doc on [service access management](https://console.bluemix.net/docs/iam/serviceidaccess.html#serviceidpolicy).

3. In the target instance, assign another policy of `writer` for the same person.


## Installing the cloning script

Working with the CLI, complete the following steps.

1. Clone the repository.
	```
	git clone https://github.com/IBM-Cloud/appid-samples.git
	```
2. Change into the script folder.
	```
	cd appid-samples/cloning-instance-with-rest
	```
3. Install the script.
	```
	sudo python setup.py install
	```

## Running the cloning script

1. Review the configurable parameters.
2. Run the following command to start the script.
	```
	appidc <source_id> <target_id> --apikey <api_key> --region <source_region> --target_region <target_region>
	```

<table>
	<tr>
		<th>Parameter</th>
		<th>Explanation</th>
	</tr>
	<tr>
		<td><i>source_id</i></td>
		<td>The tenantID of the source instance of App ID that you want to clone.</td>
	</tr>
	<tr>
		<td><i>target_id</i></td>
		<td>The tenantID of the target instance of App ID that you want to copy the configuration to.</td>
	</tr>
	<tr>
		<td><i>api_key</i></td>
		<td>The API key used to create an IAM token with sufficient privileges.</td>
	</tr>
	<tr>
		<td><i>source_region</i></td>
		<td>The region that the instance of App ID that you want to clone is located in. If not provided, the default is US-South.</td>
	</tr>
	<tr>
		<td><i>target_region</i></td>
		<td>The region that the instance of App ID that you want to copy the configuration to is located in. If not provided, it will default to the source region.</td>
	</tr>
</table>

		>Tip: To see the REST messages, append the `-v` flag to the command.


So, say you have App ID instance, x, that you have configured exactly as you want it but you need the same configuration in instance y. Both instances of the service are located in the IBM Cloud UK region. What would that command look like? Check out the following example.

Example: 
```
appidc xxxxxxx yyyyyyy --apikey KkKkKkKkkKkKkKkKk --region eu-gb
```

And that's it! 

To go even further with App ID and access management, check out [our documentation](https://console.bluemix.net/docs/services/appid/api-reference.html)!
