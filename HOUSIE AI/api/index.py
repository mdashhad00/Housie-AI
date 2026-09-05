"""
Vercel Serverless Function Entry Point for Housie AI
This file imports the Flask app from the parent directory and exposes it
as a Vercel-compatible serverless handler.
"""
import sys
import os

# Add the project root to Python path so imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
