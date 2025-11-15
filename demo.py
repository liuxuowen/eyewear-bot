"""
Demo script to show the eyewear bot functionality
This script demonstrates the message formatting without requiring database connection
"""
from datetime import datetime, timedelta
from message_formatter import format_stats_message, format_daily_report, format_today_report, format_recent_days_report


def demo_daily_report():
    """Demo daily report message"""
    print("\n" + "=" * 60)
    print("示例 1: 每日自动报告 (12:01 AM)")
    print("=" * 60)
    
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    stats = {
        'start_date': yesterday,
        'end_date': yesterday,
        'leads': {
            'total_leads': 32,
            'by_sales': [
                {'sales': '张三', 'leads_count': 12},
                {'sales': '李四', 'leads_count': 11},
                {'sales': '王五', 'leads_count': 9}
            ]
        },
        'orders': {
            'total_orders': 10,
            'by_sales': [
                {'sales': '张三', 'orders_count': 5, 'total_sales': 18500.00},
                {'sales': '李四', 'orders_count': 3, 'total_sales': 11200.00},
                {'sales': '王五', 'orders_count': 2, 'total_sales': 6800.00}
            ]
        }
    }
    
    message = format_daily_report(stats)
    print(message)


def demo_today_query():
    """Demo today's query response"""
    print("\n" + "=" * 60)
    print("示例 2: 用户查询 - 今日")
    print("=" * 60)
    print("用户在群里发送: @机器人 今日")
    print("-" * 60)
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    stats = {
        'start_date': today,
        'end_date': today,
        'leads': {
            'total_leads': 15,
            'by_sales': [
                {'sales': '张三', 'leads_count': 6},
                {'sales': '李四', 'leads_count': 5},
                {'sales': '王五', 'leads_count': 4}
            ]
        },
        'orders': {
            'total_orders': 5,
            'by_sales': [
                {'sales': '张三', 'orders_count': 3, 'total_sales': 9800.00},
                {'sales': '李四', 'orders_count': 2, 'total_sales': 6500.00}
            ]
        }
    }
    
    message = format_today_report(stats)
    print(message)


def demo_recent_days_query():
    """Demo recent days query response"""
    print("\n" + "=" * 60)
    print("示例 3: 用户查询 - 最近7日")
    print("=" * 60)
    print("用户在群里发送: @机器人 最近7日")
    print("-" * 60)
    
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=6)).strftime('%Y-%m-%d')
    
    stats = {
        'start_date': start_date,
        'end_date': end_date,
        'leads': {
            'total_leads': 156,
            'by_sales': [
                {'sales': '张三', 'leads_count': 62},
                {'sales': '李四', 'leads_count': 51},
                {'sales': '王五', 'leads_count': 43}
            ]
        },
        'orders': {
            'total_orders': 48,
            'by_sales': [
                {'sales': '张三', 'orders_count': 21, 'total_sales': 82500.00},
                {'sales': '李四', 'orders_count': 16, 'total_sales': 59800.00},
                {'sales': '王五', 'orders_count': 11, 'total_sales': 38200.00}
            ]
        }
    }
    
    message = format_recent_days_report(stats, 7)
    print(message)


def demo_help_message():
    """Demo help message for unknown queries"""
    print("\n" + "=" * 60)
    print("示例 4: 未知查询 - 帮助信息")
    print("=" * 60)
    print("用户在群里发送: @机器人 帮助")
    print("-" * 60)
    
    help_message = """❓ 未知查询格式

支持的查询命令:
• 今日 - 查询今日的订单和线索数据
• 最近n日 - 查询最近n天的数据（例如：最近7日）

示例:
@机器人 今日
@机器人 最近7日
@机器人 最近30日"""
    
    print(help_message)


def main():
    """Run all demos"""
    print("\n")
    print("🤖 眼镜电商企业微信机器人 - 功能演示")
    print("=" * 60)
    
    demo_daily_report()
    demo_today_query()
    demo_recent_days_query()
    demo_help_message()
    
    print("\n" + "=" * 60)
    print("✅ 演示完成")
    print("=" * 60)
    print("\n提示:")
    print("- 所有数据示例均为模拟数据")
    print("- 实际使用时需要配置数据库和企业微信机器人")
    print("- 详细配置说明请参考 README.md")
    print()


if __name__ == '__main__':
    main()
