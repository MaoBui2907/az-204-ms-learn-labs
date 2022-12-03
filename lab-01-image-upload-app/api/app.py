import os
import flask
from flask import jsonify
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

app = flask.Flask(__name__)
connection_string = os.environ.get('blob_storage')
blob_client = BlobServiceClient.from_connection_string(conn_str=connection_string)

@app.route('/', methods=['GET'])
def home():
    return '''
        <h1>Image Uploading</h1>
    '''

@app.route('/api/images', methods=['GET'])
def get_images():
    container = [container for container in blob_client.list_containers() if container.name == 'images'][0]
    container_client = blob_client.get_container_client(container)
    images = container_client.list_blobs()
    for image in images:
        print(image)
    return jsonify({'response': 200, 'data': []})

if __name__ == "__main__":
    app.run(debug=True)