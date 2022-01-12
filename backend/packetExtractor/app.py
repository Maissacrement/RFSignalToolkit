#!/usr/bin/env python3
from flask import Flask, Response, request
import json
from flask_cors import CORS,cross_origin


app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/dynmagnet', methods=['POST', 'GET'])
def dyns():
    return []

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host="0.0.0.0")