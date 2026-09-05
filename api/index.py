"""
Serverless Function Entry Point for Housie AI on Vercel
"""
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from flask import Flask, request, jsonify
from flask_cors import CORS
import app as housie_core

app = Flask(__name__)
CORS(app)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'OPTIONS'])
def catch_all(path):
    if request.method == 'OPTIONS':
        return '', 200
    if request.method == 'GET':
        return jsonify({
            'status': 'online',
            'name': 'Housie AI API',
            'version': '4.0'
        })
    return housie_core.chat()
