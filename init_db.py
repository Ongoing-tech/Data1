from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 初始化数据库
    db = SQLAlchemy(app)
    
    # 定义数据模型
    class InventoryData(db.Model):
        __tablename__ = 'inventory_data'
        
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        date = db.Column(db.Date, nullable=False, index=True)
        sku = db.Column(db.String(50), nullable=False, index=True)
        product_name = db.Column(db.String(200), nullable=True)
        inbound_quantity = db.Column(db.Integer, nullable=True, default=0)
        outbound_quantity = db.Column(db.Integer, nullable=True, default=0)
        inventory_balance = db.Column(db.Integer, nullable=True, default=0)
        supplier = db.Column(db.String(100), nullable=True, index=True)
        operator = db.Column(db.String(50), nullable=True)
        remarks = db.Column(db.Text, nullable=True)
        created_at = db.Column(db.DateTime, default=db.func.now())
        updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
        
        # 创建复合唯一索引，防止相同日期和SKU的数据重复
        __table_args__ = (
            db.UniqueConstraint('date', 'sku', name='uq_date_sku'),
            db.Index('idx_date_sku', 'date', 'sku'),
            db.Index('idx_supplier_date', 'supplier', 'date'),
        )
        
        def to_dict(self):
            return {
                'id': self.id,
                'date': self.date.strftime('%Y-%m-%d') if self.date else None,
                'sku': self.sku,
                'product_name': self.product_name,
                'inbound_quantity': self.inbound_quantity,
                'outbound_quantity': self.outbound_quantity,
                'inventory_balance': self.inventory_balance,
                'supplier': self.supplier,
                'operator': self.operator,
                'remarks': self.remarks,
                'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
                'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
            }
    
    return app, db, InventoryData

def init_database():
    app, db, InventoryData = create_app()
    
    with app.app_context():
        try:
            # 创建所有表
            db.create_all()
            print("数据库表创建成功！")
            
            # 验证表是否创建成功
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"已创建的表: {', '.join(tables)}")
            
        except Exception as e:
            print(f"数据库初始化失败: {str(e)}")
            sys.exit(1)

if __name__ == '__main__':
    print("开始初始化数据库...")
    init_database()
    print("数据库初始化完成！")