import sys
import os
from serverless_wsgi import handle_request

# 将项目根目录添加到 Python 路径，确保可以导入你的 Flask app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# 从你的主应用文件中导入 Flask 应用对象
from app import app

def handler(event, context):
    """ Netlify Function 的入口处理程序 """
    return handle_request(app, event, context)