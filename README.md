# 图书搜索API说明文档

## 概述
此API提供图书搜索功能，可根据多个关键词在数据库中检索相关图书信息。系统支持自动创建数据表，优化了错误处理，提供了Web界面。

## 服务端要求
- Python 3.6+
- Flask
- mysql-connector-python
- python-dotenv

## 安装依赖
```bash
pip install flask mysql-connector-python python-dotenv requests
```

## 配置
在项目根目录创建`.env`文件，配置以下环境变量：
```
# 数据库配置
DB_HOST=数据库主机
DB_PORT=数据库端口
DB_USER=数据库用户名
DB_PASSWORD=数据库密码
DB_NAME=数据库名称

# 应用配置
PORT=5000
DEBUG=False
```

## 数据库
系统使用MySQL数据库，会自动创建必要的表结构：

```sql
CREATE TABLE IF NOT EXISTS news_book_relation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_name VARCHAR(255),
    book_introduction TEXT,
    keywords TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)
```

注意：用户需要有创建表的权限。

## 运行API服务
```bash
python book_api.py
```
服务将根据环境变量配置在指定端口上启动。

## 使用方式

### 1. Web界面
启动服务后，访问 http://localhost:5000 (或对应服务器地址)，可使用网页界面进行图书搜索。

### 2. API调用

#### 搜索图书
- **URL**: `/search`
- **方法**: POST
- **请求体格式**: JSON

#### 请求参数

| 序号 | 参数名 | 类型 | 说明 |
|------|--------|------|------|
| 1 | sqlcount | 数字 | 限制返回结果数量，范围1-100，默认10 |
| 2 | key1 | 文本 | 第一个搜索关键词 |
| 3 | key2 | 文本 | 第二个搜索关键词 |
| 4 | key3 | 文本 | 第三个搜索关键词 |
| 5 | key4 | 文本 | 第四个搜索关键词 |
| 6 | key5 | 文本 | 第五个搜索关键词 |

#### 返回结果
- 成功：JSON格式的数组，每个数组元素对应一条图书记录
- 错误：包含错误信息的JSON对象，HTTP状态码非200

#### 错误处理
API会返回友好的错误消息，包括：
- 数据库连接错误
- 表不存在错误（会尝试自动创建表）
- 访问权限错误
- 请求格式错误

#### 请求示例
```json
{
  "sqlcount": 10,
  "key1": "小说",
  "key2": "科技",
  "key3": "历史",
  "key4": "",
  "key5": ""
}
```

### 3. 测试脚本
可以使用提供的测试脚本`test_book_api.py`来测试API：
```bash
python test_book_api.py
```

## 主要优化
1. 使用环境变量管理配置，提高安全性
2. 使用数据库连接池，提高性能
3. 动态构建SQL查询，只查询非空关键词
4. 增加输入验证和错误处理
5. 日志记录，便于调试和监控
6. 自动创建数据表，简化部署
7. 提供Web界面，方便用户使用
8. 友好的错误提示，改善用户体验 