import time

from dotenv import load_dotenv

from configs.config import azure_congnitive_services_config
from azure.storage.blob import BlobServiceClient
import os

load_dotenv()

# Function to save the uploaded audio file
def save_streamlit_audio_to_local_file(uploaded_file):
    try:
        # get mount path form environment variable
        mount_path = os.getenv("MOUNT_PATH")

        epoch_time = int(time.time())
        file_path = f"{mount_path}/user_audio_{epoch_time}.wav"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        # return the full file path

        return file_path
    except Exception as e:
        print(f"Error saving audio: {e}")
        raise Exception(f"Error saving audio: {e}")

# Function to upload file to Azure Blob Storage
def upload_to_azure(file_path):
    storage_connection_string = azure_congnitive_services_config["blob_service_connection_string"]
    container_name = azure_congnitive_services_config["blob_container_name"]

    blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_path)

        # Upload the file
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        print(f"File uploaded to Azure Blob Storage: {file_path}")
        blob_url = blob_client.url
        print("Blob URL:", blob_url)
        return blob_url
    except Exception as e:
        print(f"Error uploading file to Azure: {e}")
        raise Exception(f"Error uploading file to Azure: {e}")


def get_downloaded_blob_file(blob_file_name):
    storage_connection_string = azure_congnitive_services_config["blob_service_connection_string"]
    container_name = azure_congnitive_services_config["blob_container_name"]

    blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_file_name)

    # add downloaded suffix to the file name
    downloaded_file_name = f"{blob_file_name.split(".")[0]}_downloaded.{blob_file_name.split('.')[1]}"
        # f"downloaded_{blob_file_name}"
            # blob_file_name.split(".")[0] + "_" + str(int(time.time())) + "." + blob_file_name.split(".")[1])
    with open(downloaded_file_name, "wb") as file:
        file.write(blob_client.download_blob().readall())

    print(f"Blob downloaded to: {downloaded_file_name}")
    return downloaded_file_name



def main():
    # Set the connection string, container name, blob name
    blob_name = "user_audio.wav"  # file which you need to download
    # Download the blob
    file_name = get_downloaded_blob_file(blob_name)
    print("File downloaded successfully:", file_name)

if __name__ == "__main__":
    main()