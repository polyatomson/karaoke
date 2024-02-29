from flask import Flask, request, jsonify
import os
from operations_w_db import get_table, record_view
app = Flask(__name__)

@app.route('/catalog', methods=['GET'])
def get_catalog():
    if request.method == 'GET':
        return get_table()

@app.route('/view', methods=['POST'])
def send_view_to_db():
    if request.method=='POST':
        song_id = request.get_json()["song_id"]
        return record_view(song_id)

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', os.environ['UI_SERVER'])
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

if __name__ == '__main__':
    app.run("localhost", os.environ['API_SERVER'])
