# Securing WebSphere Liberty apps running in Kubernetes with App ID

So, you have a server side Java application and you need to be able to authenticate your users without the hassle? Then [App ID](https://www.ibm.com/blogs/bluemix/2017/03/introducing-ibm-bluemix-app-id-authentication-profiles-service-app-developers/) is for you. There's no easier way to create a scalable app than to use the nimble IBM WebSphere Liberty application server in a Docker image and run it with [IBM Cloud Container Service](/docs/containers/container_index.html#container_index).


## Prerequisites

Before you can get started, you'll need to complete the following prerequisites.

* Install the required CLIs and create a lite cluster. To work with the IBM Cloud Container Service, you'll need to install the IBM Cloud CLI, the Docker CLI, the Kubernetes CLI, the IBM Cloud Container Service plugin and the IBM Cloud Container Registry plugin. You can follow this easy to use [Creating clusters](https://console.bluemix.net/docs/containers/cs_tutorials.html#cs_cluster_tutorial) tutorial for a step by step guide.
* Create an image repository namespace. You follow steps 1 through 4 of the tutorial [Deploying apps into clusters](https://console.bluemix.net/docs/containers/cs_tutorials_apps.html#cs_apps_tutorial) for help.
* Install [Maven](https://maven.apache.org/download.cgi). This is required to build the provided sample.


## Configuring the sample

You should now have the CLIs installed, a lite cluster, and an image repository namespace in IBM Cloud Container Registry. The following steps assume that you are using the default cluster namespace. Pro tip: Don't confuse the image repository namespace and the cluster namespace. They are different namespaces.

Pro tip: To use a different cluster namespace, add the *--namespace=* parameter to the kubectl commands.


1. In your terminal, log in to IBM Cloud.

	```
	bx login
	```

2. Run the following command

	```
	CLUSTER_NAME=<your Kubernetes cluster name>
	bx cs cluster-config $CLUSTER_NAME
	```
The output would be `export KUBECONFIG=...`. Copy and paste it at your terminal to set this variable to your env.

3. Replace the variables in the following commands with the values appropriate for your app and execute them in terminal.
	- Set a value to region where you want to create the App ID instance at. This should match the region you used when creating the cluster and repository namespace. Call `bx regions` for a list of available regions and set the selected name:

     ```
	    REGION=<region name, e.g. us-south>  
	 ```

	- Set the domain for your containers registry, according to the region you selected. See:  [registry regions](https://console.bluemix.net/docs/services/Registry/registry_overview.html#registry_regions) for available registries domains

	 ```
	 REGISTRY_DOMAIN=<registry domain, e.g. registry.ng.bluemix.net>  
	 ```
	   
	- Set you repository namespace. Call `bx cr namespaces` for a list of available namesapces  
	    
	  ```
	  REPOSITORY_NAMESPACE=<your repository namespace>
	  ```

	- Set the name of your app ID instance
        ```
        APPID_INSTANCE_NAME=<your choice of an App ID instance name>  
		```


4. Create an instance of App ID.

	<!--CF (this is what currently supported):-->
	```
	bx service create appid "Graduated tier" $APPID_INSTANCE_NAME
	```
	<!--RC (will start using this command once App ID is RC compatible in production):
	```
	bx resource service-instance-create $APPID_INSTANCE_NAME appid graduated-tier $REGION
	``` -->
5. *Optional*: Configure your App ID preferences. In the output of the following command, click on the Dashboard URL.

	```
	bx service show $APPID_INSTANCE_NAME
	```
6. Bind the instance of App ID that you created to your cluster.

	```
	bx cs cluster-service-bind $CLUSTER_NAME default $APPID_INSTANCE_NAME
	```
7. Get the sample source from github repository [appid-samples](https://github.com/IBM-Cloud/appid-samples) or clone it: 
    ```
    git clone git@github.com:IBM-Cloud/appid-samples.git
    ```
    then go into the appid-liberty-docker folder
    ```
    cd appid-liberty-docker
    ```
8. Change directories so that you're in the folder in which you extracted the sample and run:

	```
	cd WebApplication; mvn clean install; cd -
	```

## Running Docker locally

Optionally, prior to pushing the sample to Kubernetes, you might want to try out running on Docker locally. When you are developing this helps you try code quickly.

1. To run locally, you need to get the App ID service instance credentials. You can get the credentials by doing one of the following:

	* Go to the **Service Credentials** tab of your instance dashboard.
	* You can decode your Kubernetes secret which you get as Base64 encoded when calling:
	          ```
				kubectl get secret binding-$APPID_INSTANCE_NAME -o json
				```

	 I have [jq](https://stedolan.github.io/jq/) installed locally so I used it to decode the value this way:
				```
				BINDING=$(kubectl get secret binding-$APPID_INSTANCE_NAME -o json | jq .data -r | jq .binding -r | base64 --decode)
				```
				**Pro tip**: This step eventually replaces the `APPID_AUTH_SERVER`, `APPID_CLIENT_ID`, `APPID_CLIENT_SECRET` and `APPID_AUTH_SERVER_ISSUER` values in your *Liberty/server.xml* with values that we append at runtime to the server *Liberty/bootstrap.properties* file. You can replace them manually, just don't pass the `--build-arg binding_secret=$BINDING` argument to the command below.

2. Run the following command to build and run the image.


			APP_VERSION=1.1
			docker rm appid_on_liberty
			docker build -t $REGISTRY_DOMAIN/$REPOSITORY_NAMESPACE/appid-liberty:$APP_VERSION . --no-cache --build-arg binding_secret=$BINDING
			docker run --name appid_on_liberty -i -p 80:9080 -p 443:9443 $REGISTRY_DOMAIN/$REPOSITORY_NAMESPACE/appid-liberty:$APP_VERSION


To see the sample running go to: [http://localhost/appidSample](http://localhost/appidSample).

You will see a page similar to the following in your browser:
![](welcomePage.jpg)

Your sample app is now configured to allow login with an identity provider, get a token from App ID's authorization endpoint, and use it to access the sample's *ProtectedServlet*.

Pro tip: To stop the server, open another terminal and run:
```
docker kill appid_on_liberty
```

## Running on IBM Cloud Container Service

You can use Kubernetes techniques in IBM Cloud Container Service to deploy apps and to ensure your apps are up and running at all times.

1. Find your cluster Public IP:
		```
		bx cs workers $CLUSTER_NAME
		```
2. Set your IP:
		```
		CLUSTER_IP=<Public IP>
		```
3. Edit the image name field of the deployment section in the **appid-liberty-sample.yml** file to match your image name. To find the name of your image:
		```
		{{REGISTRY_DOMAIN}}/{{REPOSITORY_NAMESPACE}}/appid-liberty:{{APP_VERSION}}
		```
4. Edit the Binding secret name field in the **appid-liberty-sample.yml** file to match yours. To find your secret name:
		```
		binding-{{APPID_INSTANCE_NAME}}
		```
5. *Optional*: Change the value of metadate.namespace from default to your cluster namespace if you're using a different namespace.

6. Build your Docker image. In an IBM Cloud Container Service *Lite* Cluster, we have to create the services with Node ports that have non standard http and https ports in the 30000-32767 range. In this example we chose http to be exposed at port 30080 and https at port 30081.
7.
	```
	APP_VERSION=1.1
	docker build -t $REGISTRY_DOMAIN/$REPOSITORY_NAMESPACE/appid-liberty:$APP_VERSION . \
	--no-cache --build-arg clusterIP=$CLUSTER_IP --build-arg sslPort=30081
	```
7. Push the image.

	```
	docker push $REGISTRY_DOMAIN/$REPOSITORY_NAMESPACE/appid-liberty:$APP_VERSION
	kubectl apply -f appid-liberty-sample.yml
	```
8. Give the server a minute to get up and running and then you'll be able to see your sample running on Kubernetes in IBM Cloud.
		```
		open http://$CLUSTER_IP:30080/appidSample
		```

## Next Steps
* Learn how to scale up your app by following this [tutorial](https://console.bluemix.net/docs/containers/cs_tutorials_apps.html#cs_apps_tutorial).
* Upgrade to an IBM Cloud standard cluster to get more options such as the ability to [expose your app to the internet with Ingress](https://console.bluemix.net/docs/containers/cs_planning.html#cs_ingress).
