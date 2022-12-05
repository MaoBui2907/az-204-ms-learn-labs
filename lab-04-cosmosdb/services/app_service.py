import os
from azure.cosmos import CosmosClient, PartitionKey
from azure.storage.blob import BlobServiceClient

class AppService:
    def __init__(self, connectionString: str, databaseName: str, blobConnectionString: str) -> None:
        self.metadataContainerName = 'MediaMetadata'
        self.cosmosClient = CosmosClient.from_connection_string(connectionString).get_database_client(databaseName)
        self.blobClient: BlobServiceClient = BlobServiceClient.from_connection_string(blobConnectionString)
        self.cosmosClient.create_container_if_not_exists(self.metadataContainerName, PartitionKey('/fileName'))
        self.mediaMetadataContainer = self.cosmosClient.get_container_client(self.metadataContainerName)
        pass

    def get_all_blob_containers(self):
        return self.blobClient.list_containers()

    def get_container_blobs(self, container: str):
        items = self.mediaMetadataContainer.read_all_items()
        return items

    def upload_media_file(self, file, container: str):
        containerClient = self.blobClient.get_container_client(container)
        containerClient.upload_blob(file)
        pass

    def upload_metadata(self, data):
        pass