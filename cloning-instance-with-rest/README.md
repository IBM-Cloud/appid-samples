# Cloning an App ID instance example

Here is an example of how to use the App ID management APIs to create a script that easily 'clones' an instance of App ID.
The script can be part of the organization DevOps pipeline and specific permissions can be granted just for this task by the IBM Cloud platform. 
We will demonstrate how the script can get an api-key to authenticate with and get the limited IAM credentials that will enable it to access App ID APIs and copy the configuration of an existing App ID instance to a newly created instance.

### Initial steps
1. The owner of the account logs in to IBM cloud console and creates a new Service ID.  See how [here](https://console.bluemix.net/docs/iam/serviceid.html#serviceids)

2. The owner will create an access policy to the service that will allow it to perform the cloning task, and will assign the platform role of an Editor and the service role of a Writer to all App ID services in the account. See how [here](https://console.bluemix.net/docs/iam/serviceidaccess.html#serviceidpolicy)

	You can read more about App ID actions and roles at [this article](https://console.stage1.bluemix.net/docs/services/appid/iam.html#service-access-management)

3. The owner will now create an api-key to this service ID, which he will later pass to the DevOps person that operates the cloning task. See how [here](https://console.bluemix.net/docs/iam/serviceid_keys.html#serviceidapikeys) 
 
For a detailed walkthrough on how to create and manage service IDs see this good [blog](https://www.ibm.com/blogs/bluemix/2017/10/introducing-ibm-cloud-iam-service-ids-api-keys/) post.

> Note: For simplicity, this example shows the cloning of an instance in the same account as the source. For cloning from one account to another, you will be creating 2 different service IDs, one in the source account and another in the target account. Then you will set the policies as appropriate so that the source will have read rights and target will have edit rights, and you will need to use the 2 different api-keys you will create in the cloning script. After you will finish this tutorial, we believe it will be a trivial addition for you to implement.

### The cloning script

Following are the steps required to create a cloning script.

1. You would need to pass to the cloning script the following: 
	1. New instance name 
	2. Service api-key
	3. Region in which to create the new instance
	4. Target resource group id
	5. App ID Plan ID for the cloned instance
	6. Source instance ID
	7. Source instance region 
	
2. You can use bx cli to get details of source instance by calling  
	`bx resource service-instance $APPID_SOURCE_INSTANCE_NAME`  
	output would be like:  
	
	```
	Name:                  <APPID_SOURCE_INSTANCE_NAME>   
	ID:                    crn:v1:bluemix:public:appid:<region>:a/<account_id>:<instance_id>::   
	Location:              <region>   
	Service Name:          appid   
	Service Plan Name:     <plan name>   
	Resource Group Name:   <source resource group name>   
	State:                 active   
	Type:                  service_instance   
	Tags:                     

	```
	
	* To get the plan id of same plan as source instance you can call:  
	`bx catalog service appid | grep <plan name>`  
	(You can also clone with a different plan available to you, choose another plan from the list in `bx catalog service appid`)  
	* You can find available regions calling IBM Cloud CLI: `bx regions`  
	* To get available resource group IDs call `bx resource groups` and copy the id of the group into which to create the cloned instance


3. In the script:  
   Get Set the name of the source App ID instance  
   
	`CLONED_APPID_INSTANCE_NAME =<cloned instance name>`   
	`CLONING_SERVICE_APIKEY=<api-key>`  
	`TARGET_REGION=<cloned instance region>`  
	`TARGET_RESOURCE_GROUP=<cloned instance group>`    
	`PLAN_ID=<Appp ID plan ID>`  
	`SOURCE_INSTANCE_ID=<source instance id>`  
	`SOURCE_INSTANCE_REGION=<source instance region>`	
    
4. Call the following REST API at the region domain of the account to get an IAM token:

    ```  
      curl -X POST \
      https://iam.ng.bluemix.net/oidc/token \
      -H 'Accept: application/json' \
      -H 'Content-Type: application/x-www-form-urlencoded' \
      -d "grant_type=urn%3Aibm%3Aparams%3Aoauth%3Agrant-type%3Aapikey&apikey=$CLONING_SERVICE_APIKEY" 
    ```
    Response would look like:
      
    ```  
    {
        "access_token": <IAM token>,  
        "refresh_token":<Refresh token>,  
        "token_type": "Bearer",  
        "expires_in": 3600,  
        "expiration": <token expiration time>  
    }
        
    ```
    
   Copy the value of `access_token` from the response
      
    `IAM_TOKEN=<IAM token>`
    
	

5. Create a new App ID service
	
    ```
    curl -X POST \
    https://resource-controller.ng.bluemix.net/v1/resource_instances \
    -H "authorization: Bearer $IAM_TOKEN" \
    -H 'content-type: application/json' \
    -d "{
      "name": "$CLONED_APPID_INSTANCE_NAME",
      "region_id": "$TARGET_REGION",
      "resource_plan_id": "$PLAN_ID",
      "resource_group_id": "$TARGET_RESOURCE_GROUP"
    }'
    ```  
     
     Response should be like:  
       
    ```
    {
        "id": "crn:v1:bluemix:public:appid:<region>:a/<account-id>::",  
        "guid": "<cloned-instance-id>",  
        "url": "/v1/resource_instances/crn%3Av1%3Abluemix%3Apublic%3Aappid%3Aregion%3Aa%2F3984162373f8850d2f9c4a0a80942828%3A28727a5f-6ec4-4588-879a-78abd0f04cd5%3A%3A",  
        "created_at": "2018-02-19T08:33:07.308113112Z",  
        "updated_at": null,  
        "deleted_at": null,  
        "name": "<instance-name>",  
        "region_id": "<region>",  
        "account_id": "<account-id>",  
        "resource_plan_id": "<plan-id>",
        "resource_group_id": "<resource-group>",
        "resource_group_crn": "crn:v1:bluemix:public:resource-controller::a/<account-id>::resource-group:<resource-group-id>",
        "target_crn": "crn:v1:bluemix:public::<region>:::environment:<env>",
        "crn": "crn:v1:bluemix:public:appid:<region>:a/<account-id>:<cloned-instance-id>::",
        "state": "active",
        "type": "service_instance",
        "resource_id": "AdvancedMobileAccess-d6aece47-d840-45b0-8ab9-ad15354deeea",
        "dashboard_url": "https://mobile.<region>.bluemix.net/imfmobileplatformdashboard?tenantId=crn%3Av1%3Abluemix%3Apublic%3Aappid%3A<region>%3Aa%2F3<account-id>%3A<cloned-instance-id>%3A%3A",
        "last_operation": null,
        "resource_aliases_url": "/v1/resource_instances/crn%3Av1%3Abluemix%3Apublic%3Aappid%3A<region>%3Aa%2F3<account-id>%3A<cloned-instance-id>%3A%3A/resource_aliases",
        "resource_bindings_url": "/v1/resource_instances/crn%3Av1%3Abluemix%3Apublic%3Aappid%3A<region>%3Aa%2F3<account-id>%3A<cloned-instance-id>%3A%3A/resource_bindings",
        "resource_keys_url": "/v1/resource_instances/crn%3Av1%3Abluemix%3Apublic%3Aappid%3A<region>%3Aa%2F3<account-id>%3A<cloned-instance-id>%3A%3A/resource_keys",
        "plan_history": [
            {
                "resource_plan_id": "<target-plan-id>",
                "start_date": "2018-02-19T08:33:07.308113112Z"
            }
        ],
        "migrated": false
    }  
     ```  
  
   set `TARGET_INSTANCE_ID=<guid from response>`
 
6. Now you should use the App ID REST API to get configuration set in source and set it in target. See the complete API documentation at: [https://appid-management.stage1.ng.bluemix.net/swagger-ui/](https://appid-management.stage1.ng.bluemix.net/swagger-ui/)

     As an example we will show how to get the IDP configuration for "facebook" from source and setting in target:
     
     Get from source:   
      
      ```
    curl -X GET \
    -H 'Accept: application/json' \
    -H "Authorization: Bearer $IAM_TOKEN" \ 
    "https://appid-management.$TARGET_REGION.bluemix.net/management/v4/$SOURCE_INSTANCE_ID/config/idps/facebook"   
      ```

    Result should be 200 and contain the IDP data, e.g.:
  
      ```
      {
          "isActive": true,
          "config": {}
      }
      ```

7. Post to target:  

   ```  
     curl -X PUT -H 'Content-Type: application/json' -H 'Accept: application/json' -H "Authorization: Bearer $IAM_TOKEN" -d '{
      "isActive": true,
      "config": {}
    }' "https://appid-management.$TARGET_REGION.bluemix.net/management/v4/$TARGET_INSTANCE_ID/config/idps/facebook" 
   ```  
   
 You can now continue this way to get other configuration elements from the original instance and putting them to the new instance that was created (as illustrated in steps #6 and #7 above), until you defined the way in which you want to 'clone' the resource.  	   
