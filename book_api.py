from flask import Flask, request, jsonify, send_from_directory
import mysql.connector
from mysql.connector import pooling
import os
import logging
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__)

# 配置日志
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 从环境变量获取数据库配置
db_config = {
    'host': os.getenv('DB_HOST', '47.122.0.231'),
    'port': os.getenv('DB_PORT', '62013'),
    'user': os.getenv('DB_USER', 'zhangzheng'),
    'password': os.getenv('DB_PASSWORD', 'Z0p9o8i7u$'),
    'database': os.getenv('DB_NAME', 'book')
}

# 创建数据库连接池
try:
    connection_pool = pooling.MySQLConnectionPool(
        pool_name="book_pool",
        pool_size=5,
        **db_config
    )
    logger.info("数据库连接池初始化成功")
except Exception as e:
    logger.error(f"数据库连接池初始化失败: {str(e)}")

# 添加根路由，提供Web界面
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/search', methods=['POST'])
def search_books():
    """图书搜索API接口"""
    conn = None
    cursor = None
    
    try:
        # 获取POST请求参数
        data = request.get_json()
        if not data:
            return jsonify({"error": "请求数据为空"}), 400
        
        # 提取并验证请求参数
        try:
            sqlcount = int(data.get('sqlcount', 10))  
            if sqlcount <= 0 or sqlcount > 100:
                sqlcount = 10  # 限制查询范围
        except (ValueError, TypeError):
            sqlcount = 10  # 默认值
            
        # 获取关键词
        keywords = []
        conditions = []
        params = []
        
        # 动态构建查询条件，只包含非空关键词
        for i in range(1, 6):
            key = data.get(f'key{i}', '').strip()
            if key:
                keywords.append(key)
                conditions.append("keywords LIKE %s OR book_name LIKE %s OR book_introduction LIKE %s")
                params.extend([f'%{key}%', f'%{key}%', f'%{key}%'])
        
        # 如果没有有效关键词，返回空结果
        if not keywords:
            return jsonify([])
        
        # 从连接池获取连接
        conn = connection_pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # 构建SQL查询语句
        query = f"""
        SELECT * FROM book300 
        WHERE {" OR ".join(conditions)}
        LIMIT %s
        """
        params.append(sqlcount)
        
        # 执行查询
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        logger.info(f"查询成功，返回 {len(results)} 条记录")
        return jsonify(results)
    
    except mysql.connector.Error as db_err:
        logger.error(f"数据库错误: {str(db_err)}")
        return jsonify({"error": "数据库查询失败", "details": str(db_err)}), 500
    
    except Exception as e:
        logger.error(f"服务器错误: {str(e)}")
        return jsonify({"error": "服务器内部错误"}), 500
    
    finally:
        # 确保资源正确关闭
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    # 生产环境应设置debug=False
    debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=debug_mode) 