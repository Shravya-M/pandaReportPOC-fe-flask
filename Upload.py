from flask import Flask, request, redirect, url_for
import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from flask_cors import CORS, cross_origin

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
CORS(app)


def blob_upload(file_data):
    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string('')

    # Create a unique name for the container
    container_name = "quickstart" + str(uuid.uuid4())

    # Create the container
    container_client = blob_service_client.create_container(container_name)

    # # Create a file in local Documents directory to upload and download
    # local_path = "./data"
    local_file_name = "quickstart" + str(uuid.uuid4()) + ".txt"

    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

    print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

    obj = file_data.read()
    blob_client.upload_blob(obj)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        print('file', file)
        print('file', file.name)
        blob_upload(file)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run(debug=True)
