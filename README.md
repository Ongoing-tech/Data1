# Excel数据管理与共享平台

## 项目概述

这是一个基于Web的Excel数据管理与共享平台，用于解决业务部门Excel数据分散、难以共享和统一查询的问题。该平台允许管理员导入固定格式的Excel数据，并提供Web界面供所有授权用户进行检索、筛选和查看。

## 功能特性

### 管理员功能
- **数据导入**: 上传.xlsx格式的Excel文件
- **文件验证**: 自动检查文件格式、大小和内容结构
- **重复数据检测**: 防止相同日期和SKU的数据重复导入
- **导入状态反馈**: 实时显示导入结果和错误信息

### 普通用户功能
- **数据查询**: 支持多条件组合查询
- **筛选功能**: 
  - 时间范围筛选（开始日期-结束日期）
  - SKU精确查询
  - 产品名称模糊查询
  - 供应商下拉选择
- **数据展示**: 表格形式展示，支持分页
- **数据可视化**: 基于查询结果生成库存余额变化趋势图

## 技术栈

- **前端**: HTML5 + CSS3 + JavaScript + Bootstrap + ECharts
- **后端**: Python 3.x + Flask
- **数据库**: MySQL 5.7+
- **Excel处理**: openpyxl
- **部署**: Nginx + Gunicorn

## 项目结构

```
Trae03/
├── app.py                 # Flask应用主文件
├── config.py             # 配置文件
├── init_db.py            # 数据库初始化脚本
├── requirements.txt      # Python依赖包
├── input.xlsx           # 示例Excel文件
├── .env                 # 环境变量配置
├── templates/           # HTML模板目录
│   ├── index.html       # 数据查询页面
│   └── upload.html      # 数据导入页面
├── static/             # 静态文件目录
│   └── js/             # JavaScript文件
│       ├── main.js     # 主页面脚本
│       └── upload.js   # 上传页面脚本
└── uploads/            # 文件上传目录（自动创建）
```

## 安装与部署

### 1. 环境准备

确保系统已安装以下软件：
- Python 3.7+
- MySQL 5.7+

### 2. 数据库配置

创建MySQL数据库用户和数据库：

```sql
CREATE DATABASE inventory_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'inventory_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON inventory_db.* TO 'inventory_user'@'localhost';
FLUSH PRIVILEGES;
```

修改配置文件 `.env`：

```env
# 数据库配置
DB_HOST=localhost
DB_USER=inventory_user
DB_PASSWORD=your_password
DB_NAME=inventory_db

# 应用配置
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 初始化数据库

```bash
python init_db.py
```

### 5. 运行应用

```bash
python app.py
```

应用将在 http://localhost:5000 启动。

## 使用说明

### 数据导入（管理员）

1. 访问 http://localhost:5000/upload
2. 点击选择文件或拖拽Excel文件到上传区域
3. 系统会自动验证文件格式和大小
4. 点击"开始上传"按钮
5. 等待处理完成，查看导入结果

### Excel模板格式要求

**必需字段**：
- `date`: 日期（YYYY-MM-DD格式）
- `sku`: 产品SKU编码（字符串）

**可选字段**：
- `product_name`: 产品名称
- `inbound_quantity`: 入库数量（整数）
- `outbound_quantity`: 出库数量（整数）
- `inventory_balance`: 库存余额（整数）
- `supplier`: 供应商名称
- `operator`: 操作员
- `remarks`: 备注信息

**示例数据**：

```csv
date,sku,product_name,inbound_quantity,outbound_quantity,inventory_balance,supplier,operator,remarks
2023-10-01,A001,智能手机,100,20,80,华为公司,张三,新品入库
2023-10-01,A002,手机壳,200,50,150,富士康,李四,常规补货
```

### 数据查询（所有用户）

1. 访问 http://localhost:5000
2. 使用筛选条件进行数据查询：
   - 设置时间范围
   - 输入SKU进行精确查询
   - 输入产品名称关键词进行模糊查询
   - 选择供应商
3. 点击"查询"按钮获取结果
4. 使用分页功能浏览数据
5. 点击"显示图表"查看库存余额变化趋势

## API接口

### 上传数据

```
POST /api/upload
Content-Type: multipart/form-data
```

**参数**：
- `file`: Excel文件

**成功响应**：
```json
{
    "code": 200,
    "message": "导入成功，共导入15条数据。"
}
```

**失败响应**：
```json
{
    "code": 400,
    "message": "导入失败：发现重复数据（SKU: ABC123, 日期: 2023-10-27）。"
}
```

### 查询数据

```
GET /api/data
```

**参数**：
- `start_date`: 开始日期（YYYY-MM-DD）
- `end_date`: 结束日期（YYYY-MM-DD）
- `sku`: SKU精确值
- `product_name_like`: 产品名称模糊匹配
- `supplier`: 供应商精确值
- `page`: 页码（默认1）
- `per_page`: 每页条数（默认20）

**成功响应**：
```json
{
    "code": 200,
    "data": {
        "items": [
            {"id": 1, "date": "2023-10-01", "sku": "A001", ...},
            {"id": 2, "date": "2023-10-01", "sku": "A002", ...}
        ],
        "total": 125,
        "page": 1,
        "per_page": 20
    }
}
```

### 获取供应商列表

```
GET /api/suppliers
```

**成功响应**：
```json
{
    "code": 200,
    "data": ["华为公司", "富士康", "小米科技"]
}
```

### 获取图表数据

```
GET /api/chart-data
```

**参数**：
- `start_date`: 开始日期（YYYY-MM-DD）
- `end_date`: 结束日期（YYYY-MM-DD）
- `sku`: SKU精确值
- `supplier`: 供应商精确值

**成功响应**：
```json
{
    "code": 200,
    "data": {
        "dates": ["2023-10-01", "2023-10-02", ...],
        "balances": [100, 80, ...]
    }
}
```

## 注意事项

- **数据唯一性**: 系统通过日期和SKU的组合来确保数据唯一性，相同日期和SKU的数据不能重复导入
- **文件限制**: 只支持.xlsx格式文件，大小限制为2MB
- **性能优化**: 在数据量小于10000条时，查询响应时间应低于2秒
- **浏览器兼容性**: 支持Chrome、Edge、Firefox的最新版本
- **安全性**: 初期版本不包含用户认证系统，建议通过网络权限控制导入页面的访问

## 故障排除

### 常见问题

#### 数据库连接失败
- 检查MySQL服务是否启动
- 验证`.env`中的数据库配置信息
- 确保数据库用户有足够的权限

#### 文件上传失败
- 确保文件格式为.xlsx
- 检查文件大小是否超过2MB
- 验证Excel文件格式是否符合模板要求

#### 导入失败：发现重复数据
- 检查Excel中是否已存在相同日期和SKU的数据
- 先删除或修改重复数据，然后重新导入

#### 图表无法显示
- 确保有查询结果数据
- 检查浏览器控制台是否有JavaScript错误
- 验证ECharts库是否正确加载

## 开发说明

### 添加新功能
- **后端API**: 在`app.py`中添加新的路由和处理函数
- **前端界面**: 在`templates`目录中创建或修改HTML文件
- **前端逻辑**: 在`static/js`目录中创建或修改JavaScript文件
- **数据库修改**: 如需修改表结构，更新`init_db.py`中的SQL语句

### 性能优化
- 数据库索引已优化，包含常用查询字段的索引
- 前端分页减少数据传输量
- 图表数据按需加载
- 建议在生产环境中使用缓存机制

## 许可证

本项目仅供学习和内部使用。