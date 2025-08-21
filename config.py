import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 数据库配置 - 使用SQLite进行测试
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'inventory_user')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'your_password')
    DB_NAME = os.getenv('DB_NAME', 'inventory_db')
    
    # 应用配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # 文件上传配置
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB
    ALLOWED_EXTENSIONS = {'xlsx'}
    
    # 使用SQLite数据库进行测试
    SQLALCHEMY_DATABASE_URI = 'sqlite:///inventory.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 10,
        'max_overflow': 20
    }