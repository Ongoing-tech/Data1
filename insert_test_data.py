from app import app, db, InventoryData
import datetime

def insert_test_data():
    with app.app_context():
        # 创建测试数据
        test_data = [
            {
                'date': datetime.date(2025, 1, 1),
                'sku': 'SKU001',
                'product_name': '产品A',
                'inbound_quantity': 100,
                'outbound_quantity': 20,
                'inventory_balance': 80,
                'supplier': '供应商A',
                'operator': '操作员1',
                'remarks': '测试数据1'
            },
            {
                'date': datetime.date(2025, 1, 2),
                'sku': 'SKU002',
                'product_name': '产品B',
                'inbound_quantity': 150,
                'outbound_quantity': 30,
                'inventory_balance': 120,
                'supplier': '供应商B',
                'operator': '操作员2',
                'remarks': '测试数据2'
            },
            {
                'date': datetime.date(2025, 1, 3),
                'sku': 'SKU003',
                'product_name': '产品C',
                'inbound_quantity': 200,
                'outbound_quantity': 50,
                'inventory_balance': 150,
                'supplier': '供应商A',
                'operator': '操作员1',
                'remarks': '测试数据3'
            }
        ]
        
        # 插入数据
        for data in test_data:
            record = InventoryData(**data)
            db.session.add(record)
        
        db.session.commit()
        print(f"成功插入{len(test_data)}条测试数据")

if __name__ == '__main__':
    insert_test_data()