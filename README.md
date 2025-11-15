# eyewear-bot
基于企业微信的机器人 - 眼镜电商数据报告系统

## 功能特性

### 1. 定时报告
- 每天凌晨 12:01 自动发送前一日的数据统计报告
- 包含总线索数、总订单数
- 包含分销售人员的线索和订单统计

### 2. 按需查询
支持在企业微信群中 @机器人 进行实时查询：
- **今日** - 返回今日的订单和线索数据总数，以及分销售的数据
- **最近n日** - 返回指定时间区间内的相应统计数据（例如：最近7日、最近30日）

## 数据表结构

### leads 表
- `leads_id` - 线索ID（主键）
- `leads_date` - 线索日期
- `sales` - 销售人员名称

### sales_orders 表
- `order_date` - 订单日期
- `sales` - 销售人员名称
- `leads_id` - 关联的线索ID（外键）
- `sales_price` - 销售金额

## 安装部署

### 1. 环境要求
- Python 3.8+
- MySQL 5.7+
- 企业微信机器人 Webhook

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置环境变量
复制 `.env.example` 为 `.env` 并填写配置：
```bash
cp .env.example .env
```

编辑 `.env` 文件：
```env
# 数据库配置
DB_HOST=your_mysql_host
DB_PORT=3306
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=eyewear_db

# 企业微信机器人配置
WECHAT_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your_webhook_key

# 服务器配置
FLASK_PORT=5000
```

### 4. 启动服务
```bash
python app.py
```

服务将在 `http://0.0.0.0:5000` 启动

## API 端点

### 健康检查
```
GET /health
```
返回服务健康状态

### Webhook 接收端点
```
POST /webhook
```
接收企业微信的消息回调

### 手动触发日报
```
POST /trigger_daily_report
```
手动触发每日报告（用于测试）

## 使用示例

### 在企业微信群中查询

1. **查询今日数据**
   ```
   @机器人 今日
   ```

2. **查询最近7天数据**
   ```
   @机器人 最近7日
   ```

3. **查询最近30天数据**
   ```
   @机器人 最近30日
   ```

### 报告格式示例

```
📊 今日数据报告
日期: 2024-01-15

==============================

📈 总线索数: 25
📦 总订单数: 8

👥 线索分销售统计:
  • 张三: 10 个线索
  • 李四: 8 个线索
  • 王五: 7 个线索

💰 订单分销售统计:
  • 张三: 4 个订单, 总额: ¥15800.00
  • 李四: 3 个订单, 总额: ¥12500.00
  • 王五: 1 个订单, 总额: ¥3200.00

==============================
```

## 项目结构

```
eyewear-bot/
├── app.py                  # 主应用程序
├── config.py               # 配置管理
├── database.py             # 数据库操作
├── wechat_bot.py          # 企业微信机器人接口
├── message_formatter.py    # 消息格式化
├── scheduler.py            # 定时任务调度
├── query_handler.py        # 查询处理器
├── requirements.txt        # Python依赖
├── .env.example           # 环境变量示例
├── .gitignore             # Git忽略文件
└── README.md              # 项目文档
```

## 企业微信配置

### 创建机器人

1. 在企业微信群中，点击右上角 "..." -> "添加群机器人"
2. 选择"自定义机器人"
3. 设置机器人名称和头像
4. 获取 Webhook 地址（格式：`https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxx`）
5. 将 Webhook 地址配置到 `.env` 文件的 `WECHAT_WEBHOOK_URL`

### 配置消息接收（可选）

如果需要接收群消息并响应查询，需要：
1. 在企业微信管理后台配置应用的接收消息服务器地址为：`http://your-server:5000/webhook`
2. 配置 Token 和 EncodingAESKey
3. 启用应用的消息接收功能

## 注意事项

1. 确保数据库表结构与代码中的查询语句匹配
2. 定时任务基于服务器本地时间，请确保服务器时区设置正确
3. 企业微信机器人有消息发送频率限制，请合理使用
4. 建议在生产环境中使用 gunicorn 或 uwsgi 部署 Flask 应用
5. 建议配置日志记录以便于故障排查

## 生产环境部署建议

### 方式一：使用 Docker (推荐)
```bash
# 使用 docker-compose 快速部署
docker-compose up -d

# 查看日志
docker-compose logs -f eyewear-bot

# 停止服务
docker-compose down
```

### 方式二：使用 Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 方式三：使用 systemd 服务
复制 `eyewear-bot.service` 到 `/etc/systemd/system/`:
```bash
sudo cp eyewear-bot.service /etc/systemd/system/
sudo systemctl enable eyewear-bot
sudo systemctl start eyewear-bot
```

查看服务状态：
```bash
sudo systemctl status eyewear-bot
```

## 故障排查

### 数据库连接失败
- 检查 `.env` 中的数据库配置是否正确
- 确认数据库服务正在运行
- 检查数据库用户权限

### 消息发送失败
- 验证 `WECHAT_WEBHOOK_URL` 是否正确
- 检查网络连接
- 查看企业微信机器人配置是否正常

### 定时任务未执行
- 检查服务器时间和时区设置
- 查看应用日志确认调度器是否启动
- 使用 `/trigger_daily_report` 端点手动测试

## 许可证

MIT License
