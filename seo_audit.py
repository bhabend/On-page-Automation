import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urljoin

# 🔐 Load API keys from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

# ✅ You can now use these securely in your functions
