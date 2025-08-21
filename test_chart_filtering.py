import requests
import json

# 测试图表数据筛选功能

def test_chart_filtering():
    print("=== 测试图表数据筛选功能 ===")
    
    # 1. 测试不带筛选的图表数据
    print("\n1. 测试不带筛选的图表数据...")
    try:
        response = requests.get('http://127.0.0.1:5000/api/chart-data')
        if response.status_code == 200:
            result = response.json()
            data = result['data']
            print(f"总数据点数: {len(data['dates'])}")
            print(f"日期范围: {data['dates'][0]} 到 {data['dates'][-1]}")
            print(f"库存余额总和: {sum(data['balances'])}")
            total_balance = sum(data['balances'])
            total_points = len(data['dates'])
        else:
            print(f"获取图表数据失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"图表数据请求失败: {e}")
        return False
    
    # 2. 测试带供应商筛选的图表数据
    print("\n2. 测试带供应商筛选的图表数据...")
    try:
        response = requests.get('http://127.0.0.1:5000/api/chart-data?supplier=供应商A')
        if response.status_code == 200:
            result = response.json()
            data = result['data']
            print(f"供应商A数据点数: {len(data['dates'])}")
            print(f"供应商A日期范围: {data['dates'][0]} 到 {data['dates'][-1]}")
            print(f"供应商A库存余额总和: {sum(data['balances'])}")
            supplier_a_balance = sum(data['balances'])
            supplier_a_points = len(data['dates'])
        else:
            print(f"获取筛选图表数据失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"筛选图表数据请求失败: {e}")
        return False
    
    # 3. 测试带另一个供应商筛选的图表数据
    print("\n3. 测试带供应商B筛选的图表数据...")
    try:
        response = requests.get('http://127.0.0.1:5000/api/chart-data?supplier=供应商B')
        if response.status_code == 200:
            result = response.json()
            data = result['data']
            print(f"供应商B数据点数: {len(data['dates'])}")
            print(f"供应商B日期范围: {data['dates'][0]} 到 {data['dates'][-1]}")
            print(f"供应商B库存余额总和: {sum(data['balances'])}")
            supplier_b_balance = sum(data['balances'])
            supplier_b_points = len(data['dates'])
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
            date_filtered_balance = sum(data['balances'])
            date_filtered_points = len(data['dates'])
        else:
            print(f"获取日期筛选图表数据失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"日期筛选图表数据请求失败: {e}")
        return False
    
    # 5. 验证筛选结果
    print("\n5. 验证筛选结果...")
    print(f"总数据点: {total_points}, 供应商A: {supplier_a_points}, 供应商B: {supplier_b_points}")
    print(f"总余额: {total_balance}, 供应商A: {supplier_a_balance}, 供应商B: {supplier_b_balance}")
    
    # 检查筛选是否有效
    if supplier_a_points < total_points and supplier_b_points < total_points:
        print("✓ 供应商筛选功能正常")
    else:
        print("✗ 供应商筛选功能异常")
        return False
    
    if date_filtered_points < total_points:
        print("✓ 日期筛选功能正常")
    else:
        print("✗ 日期筛选功能异常")
        return False
    
    print("\n=== 所有筛选测试通过 ===")
    return True

if __name__ == '__main__':
    test_chart_filtering()