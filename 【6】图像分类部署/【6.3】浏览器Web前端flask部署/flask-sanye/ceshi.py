from sqlalchemy import create_engine

# 创建数据库引擎
engine = create_engine('mysql+pymysql://root:wht050106@localhost:3306/sanye_qing?charset=utf8')

# 尝试连接到数据库
try:
    connection = engine.connect()
    print("Connection successful!")
    connection.close()
except Exception as e:
    print("Error connecting to the database:", e)
