# 快速入门指南 (Quick Start Guide)

## 系统要求

- Python 3.8+
- MySQL 5.7+
- 企业微信账号和机器人

## 快速部署

### 1. 克隆代码
```bash
git clone https://github.com/liuxuowen/eyewear-bot.git
cd eyewear-bot
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置环境
```bash
cp .env.example .env
# 编辑 .env 文件，填入实际配置
```

### 4. 初始化数据库
```bash
# 使用 schema.sql 创建数据表
mysql -u your_user -p your_database < schema.sql
```

### 5. 启动服务
```bash
python app.py
```

## 功能测试

### 运行功能演示
```bash
python demo.py
```
查看机器人的消息格式示例

### 运行基础测试
```bash
python test_basic.py
```
验证核心功能正常工作

### 测试定时任务
```bash
curl -X POST http://localhost:5000/trigger_daily_report
```
手动触发每日报告

### 健康检查
```bash
curl http://localhost:5000/health
```
检查服务状态

## 企业微信配置

### 方式一：群机器人（推荐用于简单场景）

1. 在企业微信群中添加机器人
2. 获取 Webhook URL
3. 配置到 `.env` 的 `WECHAT_WEBHOOK_URL`

**优点**：配置简单，无需开发者认证
**缺点**：只能主动发送消息，不能接收@消息

### 方式二：企业微信应用（支持完整交互）

1. 创建企业微信应用
2. 配置接收消息服务器：`http://your-server:5000/webhook`
3. 配置 Token 和 EncodingAESKey
4. 启用消息接收功能

**优点**：支持接收用户@消息，实现完整交互
**缺点**：配置相对复杂

## 常见问题

### Q: 如何修改定时报告的时间？
A: 编辑 `scheduler.py` 文件中的 cron 表达式：
```python
scheduler.add_job(
    daily_report_job,
    'cron',
    hour=0,    # 小时 (0-23)
    minute=1,  # 分钟 (0-59)
    ...
)
```

### Q: 如何添加更多查询命令？
A: 在 `query_handler.py` 中的 `process_query` 方法添加新的查询匹配规则

### Q: 数据库连接失败怎么办？
A: 
1. 检查 `.env` 配置是否正确
2. 确认数据库服务正在运行
3. 验证用户权限：`GRANT ALL ON eyewear_db.* TO 'user'@'localhost';`

### Q: 消息发送失败？
A: 
1. 验证 Webhook URL 是否正确
2. 检查网络连接
3. 确认机器人未被禁用

## 生产环境部署

### 使用 Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 使用 Supervisor 守护进程
```ini
[program:eyewear-bot]
command=/path/to/venv/bin/python /path/to/eyewear-bot/app.py
directory=/path/to/eyewear-bot
user=your_user
autostart=true
autorestart=true
stderr_logfile=/var/log/eyewear-bot.err.log
stdout_logfile=/var/log/eyewear-bot.out.log
```

### 使用 Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

## 日志和监控

建议添加日志配置：
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
```

## 扩展功能建议

1. **数据可视化**：添加图表生成功能
2. **导出报告**：支持 Excel/PDF 导出
3. **告警功能**：异常数据自动提醒
4. **多维度分析**：按产品、地区等维度统计
5. **历史对比**：同比、环比分析

## 技术支持

- GitHub Issues: https://github.com/liuxuowen/eyewear-bot/issues
- 企业微信开发文档: https://developer.work.weixin.qq.com/
