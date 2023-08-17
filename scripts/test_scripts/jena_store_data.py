import requests

fuseki_url = "http://64.225.131.120:9999"
dataset_name = "aqqa"
file_path = f"/mnt/data/processed/RDF/GADM/gadm_germany.ttl"

username = "admin"
password = "RJNpCnRR955D4mB"

# Upload TTL file to the dataset
def upload_ttl_to_dataset():
    upload_url = f"{fuseki_url}/{dataset_name}/data"
    
    with open(file_path, "rb") as ttl_file:
        files = {"file": (file_path, ttl_file)}
        auth = (username, password)
        response = requests.post(upload_url, files=files, auth=auth)
        
        if response.status_code == 200:
            print("TTL file uploaded successfully.")
        else:
            print("Error uploading TTL file:", response.text)

upload_ttl_to_dataset()