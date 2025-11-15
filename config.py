"""
Configuration module for the eyewear bot
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', ''),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'eyewear_db'),
    'charset': 'utf8mb4'
}

# WeChat Configuration
WECHAT_WEBHOOK_URL = os.getenv('WECHAT_WEBHOOK_URL', '')

# Server Configuration
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
