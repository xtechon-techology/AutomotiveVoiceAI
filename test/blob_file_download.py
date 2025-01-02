import time
from configs.config import azure_congnitive_services_config
from azure.storage.blob import BlobServiceClient


def get_downloaded_blob_file(blob_file_name):
    storage_connection_string = azure_congnitive_services_config["blob_service_connection_string"]
    container_name = azure_congnitive_services_config["blob_container_name"]

    blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_file_name)

    # unique file name with epoch timestamp as suffix
    downloaded_file_name = blob_file_name.split(".")[0] + "_" + str(int(time.time())) + "." + blob_file_name.split(".")[1]
    with open(downloaded_file_name, "wb") as file:
        file.write(blob_client.download_blob().readall())

    print(f"Blob downloaded to: {downloaded_file_name}")
    return downloaded_file_name


# Set the connection string, container name, blob name

blob_name = "user_audio.wav"  # file which you need to download

# Download the blob
file_name = get_downloaded_blob_file(blob_name)
print("File downloaded successfully:", file_name)
