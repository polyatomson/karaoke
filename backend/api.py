from flask import Flask, request, jsonify
import os
app = Flask(__name__)

@app.route('/catalog', methods=['GET'])
def get_catalog():
    if request.method == 'GET':
        return 'ok'
    

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', os.environ['UI_SERVER'])
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

if __name__ == '__main__':
    app.run("localhost", os.environ['API_SERVER'])
