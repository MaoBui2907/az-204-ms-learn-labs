import os
from treelib import Tree
from azure.identity import ClientSecretCredential, DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


class BlobStorageService:
    def __init__(self, endpoint: str, tenantId: str, accountName: str, accountKey: str) -> None:
        credential = ClientSecretCredential(
            tenant_id=tenantId,
            client_id=accountName,
            client_secret=accountKey
        )
        credential = DefaultAzureCredential()
        self.blobServiceClient = BlobServiceClient(
            account_url=endpoint,
            credential=credential
        )
    
    def get_account_info(self):
        try:
            account = self.blobServiceClient.get_account_information()
            return account
        except:
            print('Not logged in by SAS')
        return None
    
    def get_containers(self):
        return self.blobServiceClient.list_containers()

    def get_blobs(self, container_name: str):
        container = self.blobServiceClient.get_container_client(container_name)
        return container.list_blobs()

    def get_blob(self, container_name: str, blob_name: str):
        container = self.blobServiceClient.get_container_client(container_name)
        blob = container.get_blob_client(blob_name)
        return blob.url

def main():
    blobStorageEndpoint = os.environ.get('STORAGE_ENDPOINT')
    tenantId = os.environ.get('TENANT_ID')
    clientId = os.environ.get('CLIENT_ID')
    clientSecret = os.environ.get('CLIENT_SECRET')
    blob_service = BlobStorageService(blobStorageEndpoint, tenantId, clientId, clientSecret)
    
    blob_tree = Tree()
    blob_tree.create_node('Blob Storage', 'blob')
    for container in blob_service.get_containers():
        if container != None: 
            blob_tree.create_node(container.name, container.name, parent='blob')
            for blob in blob_service.get_blobs(container.name):
                if blob != None:
                    blob_tree.create_node('{}: {}'.format(blob.name, blob_service.get_blob(container.name, blob.name)), blob.name, parent=container.name)
    
    blob_tree.show()

if __name__ == '__main__':
    main()