"""
Vercel Serverless Function Handler for AetherCrypt FastAPI Backend
"""

import sys
from pathlib import Path

# Add backend directory to sys.path so modules in backend/core can be imported seamlessly
root_dir = Path(__file__).resolve().parent.parent
backend_dir = root_dir / "backend"

if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Import the existing FastAPI app from backend.main
from main import app

# Vercel looks for the ASGI/WSGI callable 'app'
# This allows all /api/* requests to be handled directly by FastAPI
