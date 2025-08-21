import datetime
import re

def parse_date_flexible(date_str):
    """灵活解析日期格式，支持多种格式"""
    date_formats = [
        '%Y-%m-%d',    # 2025-08-20
        '%Y/%m/%d',    # 2025/08/20
        '%Y.%m.%d',    # 2025.08.20
        '%Y%m%d',      # 20250820
        '%d-%m-%Y',    # 20-08-2025
        '%d/%m/%Y',    # 20/08/2025
        '%d.%m.%Y',    # 20.08.2025
        '%m-%d-%Y',    # 08-20-2025
        '%m/%d/%Y',    # 08/20-2025
        '%m.%d.%Y',    # 08.20.2025
    ]
    
    # 先尝试标准格式
    for fmt in date_formats:
        try:
            return datetime.datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    
    # 如果标准格式失败，尝试处理单数字月份和日期
    # 处理 YYYY/M/D 格式
    if re.match(r'^\d{4}/\d{1,2}/\d{1,2}$', date_str):
        parts = date_str.split('/')
        if len(parts) == 3:
            try:
                year = int(parts[0])
                month = int(parts[1])
                day = int(parts[2])
                return datetime.date(year, month, day)
            except ValueError:
                pass
    
    # 处理 YYYY-M-D 格式
    if re.match(r'^\d{4}-\d{1,2}-\d{1,2}$', date_str):
        parts = date_str.split('-')
        if len(parts) == 3:
            try:
                year = int(parts[0])
                month = int(parts[1])
                day = int(parts[2])
                return datetime.date(year, month, day)
            except ValueError:
                pass
    
    # 处理 YYYY.M.D 格式
    if re.match(r'^\d{4}\.\d{1,2}\.\d{1,2}$', date_str):
        parts = date_str.split('.')
        if len(parts) == 3:
            try:
                year = int(parts[0])
                month = int(parts[1])
                day = int(parts[2])
                return datetime.date(year, month, day)
            except ValueError:
                pass
    
    # 处理 D-M-YYYY 格式
    if re.match(r'^\d{1,2}-\d{1,2}-\d{4}$', date_str):
        parts = date_str.split('-')
        if len(parts) == 3:
            try:
                day = int(parts[0])
                month = int(parts[1])
                year = int(parts[2])
                return datetime.date(year, month, day)
            except ValueError:
                pass
    
    # 处理 D/M/YYYY 格式
    if re.match(r'^\d{1,2}/\d{1,2}/\d{4}$', date_str):
        parts = date_str.split('/')
        if len(parts) == 3:
            try:
                day = int(parts[0])
                month = int(parts[1])
                year = int(parts[2])
                return datetime.date(year, month, day)
            except ValueError:
                pass
    
    # 处理 D.M.YYYY 格式
    if re.match(r'^\d{1,2}\.\d{1,2}\.\d{4}$', date_str):
        parts = date_str.split('.')
        if len(parts) == 3:
            try:
                day = int(parts[0])
                month = int(parts[1])
                year = int(parts[2])
                return datetime.date(year, month, day)
            except ValueError:
                pass
    
    return None

# 测试日期解析功能
test_dates = [
    '2025/1/5',    # 用户提到的格式
    '2025-1-5',    # 短横线格式
    '2025.1.5',    # 点号格式
    '2025/01/05',  # 标准格式
    '2025-01-05',  # 标准格式
    '5-1-2025',    # 日-月-年格式
    '5/1/2025',    # 日/月/年格式
    '5.1.2025',    # 日.月.年格式
]

print("测试日期解析功能：")
for date_str in test_dates:
    result = parse_date_flexible(date_str)
    print(f"{date_str} -> {result}")