from app import app, db, InventoryData
import sys

def recreate_database():
    with app.app_context():
        try:
            # 删除所有表
            db.drop_all()
            print("已删除所有表")
            
            # 重新创建所有表
            db.create_all()
            print("数据库表重新创建成功！")
            
            # 验证表是否创建成功
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"已创建的表: {', '.join(tables)}")
            
        except Exception as e:
            print(f"数据库重建失败: {str(e)}")
            sys.exit(1)

if __name__ == '__main__':
    print("开始重建数据库...")
    recreate_database()
    print("数据库重建完成！")