import openpyxl
from openpyxl import Workbook

# 创建一个新的Excel工作簿
wb = Workbook()
ws = wb.active
ws.title = "库存数据"

# 添加标题行
headers = ["日期", "SKU", "产品名称", "入库数量", "出库数量", "库存余额", "供应商", "操作员", "备注"]
ws.append(headers)

# 添加测试数据，包含用户提到的日期格式
test_data = [
    ["2025/1/5", "SKU001", "测试产品1", 100, 0, 100, "供应商A", "张三", "测试数据"],
    ["2025/1/6", "SKU002", "测试产品2", 50, 10, 40, "供应商B", "李四", "测试数据"],
    ["2025/1/7", "SKU003", "测试产品3", 200, 50, 150, "供应商A", "王五", "测试数据"],
    ["2025-1-8", "SKU004", "测试产品4", 80, 20, 60, "供应商C", "赵六", "测试数据"],
    ["2025.1.9", "SKU005", "测试产品5", 150, 30, 120, "供应商B", "钱七", "测试数据"],
]

for row in test_data:
    ws.append(row)

# 保存文件
wb.save("test_upload.xlsx")
print("测试Excel文件已创建：test_upload.xlsx")