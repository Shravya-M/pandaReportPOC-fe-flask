from flask import Flask, request, redirect, url_for, jsonify
import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from flask_cors import CORS, cross_origin
import traceback, sys
from analysis import get_EDA
import pickle
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.datastructures import FileStorage
from analysis import get_EDA

ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

connection_string = "DefaultEndpointsProtocol=https;AccountName=testcopyfunction;AccountKey=766qjrMLxSfRbHNpAwd82D4YEnWHCAKk3gTLS/s/+c+BkUyTYLDN5hVc6xPuvAYl2PHLOjXrIK02O8lncEKK4Q==;EndpointSuffix=core.windows.net"
container_name = "myblockblob"
def get_EDA_helper(file_path, blob_name):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        with open(file_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
        result =  { "report": get_EDA(file_path), "status": "success"}
        # print(result)
        return result
    except Exception as e:
        tb = sys.exc_info()[-1]
        print(f'Error: {str(e)} in line {tb.tb_lineno} in function: {traceback.extract_tb(tb, 1)[0][2]}')
        return {"status": "fail", 'ERROR': f'Error: {str(e)} in line {tb.tb_lineno} in function: {traceback.extract_tb(tb, 1)[0][2]}'}

@app.route('/getList', methods=['GET'])
def getClients():
    #get clients in container
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        blobs = []
        for blob in container_client.list_blobs():
            blobs.append(blob['name'])
        return {"status": "success", "listBlobs": blobs }
    except Exception as e:
        tb = sys.exc_info()[-1]
        # print(f'Error: {str(e)} in line {tb.tb_lineno} in function: {traceback.extract_tb(tb, 1)[0][2]}')
        return {"status": "fail", "reason": f'Error: {str(e)} in line {tb.tb_lineno} in function: {traceback.extract_tb(tb, 1)[0][2]}' }

@app.route('/upload', methods=['POST', "GET"])
def upload_file():
    try:
        if request.method == 'POST':
            imd = ImmutableMultiDict(request.files)
            result = imd.to_dict(flat=False) ['ipfile'][0]
            # print(result, result.filename)
            result.save(result.filename)
            local_path = "/Users/s0m0961/Documents/flask-poc19/"
            upload_file_path = os.path.join(local_path, result.filename)
            # blob_service_client = BlobServiceClient.from_connection_string(connection_string)
            # blob_client = blob_service_client.get_blob_client(container=container_name, blob=result.filename)
            # with open(upload_file_path, "rb") as data:
            #     blob_client.upload_blob(data, blob_type="BlockBlob", overwrite=True)
            report = get_EDA_helper(upload_file_path, result.filename)
            if report['status'] == "success":
                return {"status": "success", "report":report['report']} 
            elif report['status'] == "fail":
                return report
    except Exception as e:
        tb = sys.exc_info()[-1]
        return {"status": "fail", "reason": f'Error: {str(e)} in line {tb.tb_lineno} in function: {traceback.extract_tb(tb, 1)[0][2]}' }

# not using this yet
@app.route('/blob', methods=['GET'])
def getBlobEDA():
    #get analysis of <blob_name> file
    try:
        blob_name = "products.csv"
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        with open(blob_name, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
            result =  { blob_name: get_EDA(blob_name), "status": "success"}
        return result
    except Exception as e:
        tb = sys.exc_info()[-1]
        print(f'Error: {str(e)} in line {tb.tb_lineno} in function: {traceback.extract_tb(tb, 1)[0][2]}')
        return {'ERROR': f'Error: {str(e)} in line {tb.tb_lineno} in function: {traceback.extract_tb(tb, 1)[0][2]}'}


if __name__ == '__main__':
    app.run(debug=True)
