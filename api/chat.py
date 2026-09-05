"""
Direct /api/chat Serverless Function for Vercel
Automatically handles POST and GET to /api/chat with zero configuration.
"""
import sys
import os

# Add root directory to Python path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import app
