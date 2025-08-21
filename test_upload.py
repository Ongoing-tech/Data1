import requests
import json

# 测试文件上传功能
url = 'http://127.0.0.1:5000/api/upload'

# 准备文件
files = {'file': open('test_upload.xlsx', 'rb')}

try:
    # 发送POST请求
    response = requests.post(url, files=files)
    
    # 打印响应
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    
    # 解析JSON响应
    if response.status_code == 200:
        result = response.json()
        print(f"响应JSON: {json.dumps(result, indent=2, ensure_ascii=False)}")
    else:
        result = response.json()
        print(f"错误信息: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
except Exception as e:
    print(f"请求失败: {e}")
finally:
    # 关闭文件
    files['file'].close()