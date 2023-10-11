
# Instructions for RDF Data Storage and Quering 

This module describes how to upload RDF data to Strabon and interact with the SPARQL endpoint by running queries to retrieve specific data from our AQ Knowledge Graph.

## Step 1: Set-Up Strabon Instance

Add steps to build docker file with right java configurations

1. **Set-Up VM on WeKeO**

For our purposes we created the following Virtual Machine (VM)
- Flavor: **eo2.2xlarge**
- VCUP: 8
- RAM: 32GB
- Storage: 128GB

We assigned a floating IP to the VM following this instructions:
- https://wekeo.docs.cloudferro.com/en/latest/networking/How-to-Add-or-Remove-Floating-IP%E2%80%99s-to-your-VM-on-WEkEO-Elasticity.html?highlight=floating%20IP

We set a rule for opening the Port 9999 following this instructions:
- https://wekeo.docs.cloudferro.com/en/latest/networking/How-can-I-open-new-ports-port-80-for-http-for-my-service-or-instance-on-WEkEO-Elasticity.html?highlight=Open%20port


2. **Important installations on VM**

Installation of gpg
```bash
sudo apt-get install gnupg
```

Install of docker following this instructions:
- https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04


3. **Clone Strabon repository from Github**

```bash
git clone https://github.com/AI-team-UoA/Strabon/tree/main
```

4. **Adjustments of Docker File. Set Java 8 as default**

```bash
# SET UP JAVA 8
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
ENV PATH $JAVA_HOME/bin:$PATH
RUN export JAVA_HOME
```

5. **Build docker image**
```bash
docker build -t strabon .
```

6. **Run strabon container**
```bash 
docker run -d eouser--name strabon-container -p 9999:8080 -v /mnt/volume:/inout strabon
```

7. **Run configuration in container and start webserver**
```bash
sudo docker exec -it strabon-container /bin/bash
```
```bash
./usr/local/bin/conf.sh
```

## Step 2: Store data in Strabon

The next step is to store the prepared RDF files in Strabon. Here we have 2 options. Either storing the data via the web interface or programmatically via HTTP requests. The following two chapters describe one of these options.

### 2.1.: Store data via Web-UI

- Enter the following URL into your browser:
<IP>:9999/Strabon
- In the `**Explore/Modify operations** section choose **Store**
- Choose RDF Format: Turtle
- Enter the Url of your datasetin URI input (requires data upload before; e.g access data at https://zenodo.org/record/8430386)
- Click **Store from URI**

<img src="images/strabon_web_ui_storage.png"
     alt="Strabon Web UI Storage"
     style="display: block; margin: 0 auto;"
     width="350" height="150" />

### 2.2.: Store data via http request

- Code to demonstrate Data Upload via HTTP request has not been successfully implemented yet. 
- In Future working code will be stored in **strabon_store_data.py** file

## Step 3: Query data

The file **strabon_query_data.py** demonstrates how you can run sparql queries against the strabon endpoint. 

Make sure that first you change the **STRABON_SPARQL_ENDPOINT** variable in the config.py file

In the folder **sparql_queries** are several examples how to query the AQQA KG. In the following chapter we will go through some of them. 


## Step 4: Explanation of selected SPARQL queries

<code>
SELECT ?subject ?predicate ?object
WHERE {
  ?subject ?predicate ?object
}
</code>


