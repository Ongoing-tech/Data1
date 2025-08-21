import requests
import json
import time

# 测试完整的上传和筛选流程

def test_upload_and_filter():
    print("=== 测试上传和筛选流程 ===")
    
    # 1. 测试文件上传
    print("\n1. 测试文件上传...")
    try:
        with open('test_upload.xlsx', 'rb') as f:
            files = {'file': f}
            response = requests.post('http://127.0.0.1:5000/api/upload', files=files)
            
        if response.status_code == 200:
            result = response.json()
            print(f"上传成功: {result['message']}")
        else:
            print(f"上传失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"上传请求失败: {e}")
        return False
    
    # 2. 测试不带筛选的图表数据
    print("\n2. 测试不带筛选的图表数据...")
    try:
        response = requests.get('http://127.0.0.1:5000/api/chart-data')
        if response.status_code == 200:
            result = response.json()
            data = result['data']
            print(f"总数据点数: {len(data['dates'])}")
            print(f"日期范围: {data['dates'][0]} 到 {data['dates'][-1]}")
            print(f"库存余额总和: {sum(data['balances'])}")
        else:
            print(f"获取图表数据失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"图表数据请求失败: {e}")
        return False
    
    # 3. 测试带供应商筛选的图表数据
    print("\n3. 测试带供应商筛选的图表数据...")
    try:
        response = requests.get('http://127.0.0.1:5000/api/chart-data?supplier=供应商A')
        if response.status_code == 200:
            result = response.json()
            data = result['data']
            print(f"供应商A数据点数: {len(data['dates'])}")
            print(f"供应商A日期范围: {data['dates'][0]} 到 {data['dates'][-1]}")
            print(f"供应商A库存余额总和: {sum(data['balances'])}")
        else:
            print(f"获取筛选图表数据失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"筛选图表数据请求失败: {e}")
        return False
    
    # 4. 测试带日期筛选的图表数据
    print("\n4. 测试带日期筛选的图表数据...")
    try:
        response = requests.get('http://127.0.0.1:5000/api/chart-data?start_date=2025-01-03&end_date=2025-01-05')
        if response.status_code == 200:
            result = response.json()
            data = result['data']
            print(f"日期筛选数据点数: {len(data['dates'])}")
            print(f"日期筛选范围: {data['dates'][0]} 到 {data['dates'][-1]}")
            print(f"日期筛选库存余额总和: {sum(data['balances'])}")
        else:
            print(f"获取日期筛选图表数据失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"日期筛选图表数据请求失败: {e}")
        return False
    
    print("\n=== 所有测试通过 ===")
    return True

if __name__ == '__main__':
    test_upload_and_filter()