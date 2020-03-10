from flask import Flask, request, redirect, url_for
import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from flask_cors import CORS, cross_origin

# from werkzeug.utils import secure_filename


# UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
CORS(app)


# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# @app.route('/')
# def hello_world():
#     return 'Hello World!'
#
#

def blob_upload(file_data):
    # AZURE_STORAGE_CONNECTION_STRING = 'DefaultEndpointsProtocol=https;AccountName=dataformatdatastorage;AccountKey' \
    #                                   '=k288LxyRHUlIsdAgs9k3XV5KvjwFoMDzDl2zVMVdwqmdMygesjhM14Zb5our' \
    #                                   '+EEJwIawP6lEyzppbHBeYH6KNQ==;EndpointSuffix=core.windows.net '
    #
    # connect_str = os.getenv(AZURE_STORAGE_CONNECTION_STRING)
    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string('')

    # Create a unique name for the container
    container_name = "quickstart" + str(uuid.uuid4())

    # Create the container
    container_client = blob_service_client.create_container(container_name)

    # # Create a file in local Documents directory to upload and download
    # local_path = "./data"
    local_file_name = "quickstart" + str(uuid.uuid4()) + ".txt"
    # upload_file_path = os.path.join(local_path, local_file_name)
    #
    # # Write text to the file
    # file = open(upload_file_path, 'w')
    # file.write("Hello, World!")
    # file.close()

    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

    print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

    # Upload the created file
    # with open(upload_file_path, "rb") as data:
    #     blob_client.upload_blob(data)

    obj = file_data.read()
    blob_client.upload_blob(obj)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        print('file', file)
        print('file', file.name)
        blob_upload(file)
    #     if file and allowed_file(file.filename):
    #         filename = secure_filename(file.filename)
    #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #         return redirect(url_for('uploaded_file',
    #                                 filename=filename))
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
