import os
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient

class AppService:
    def __init__(self, connectionString: str, databaseName: str, blobConnectionString: str) -> None:
        self.cosmosClient = CosmosClient.from_connection_string(connectionString).get_database_client(databaseName)
        self.blobClient = BlobServiceClient.from_connection_string(blobConnectionString)
        pass

    def get_all_blob_containers(self):
        return self.blobClient.list_containers()

    def upload_media_file(self, file):
        pass

    def upload_metadata(self, data):
        pass