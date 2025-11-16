"""
Message formatter module
"""
from datetime import datetime


def format_stats_message(stats, title="数据统计报告"):
    """
    Format statistics data into a readable message
    
    Args:
        stats: Statistics dictionary containing leads and orders data
        title: Title for the message
        
    Returns:
        str: Formatted message
    """
    start_date = stats.get('start_date', '')
    end_date = stats.get('end_date', '')
    leads = stats.get('leads', {})
    orders = stats.get('orders', {})
    
    # Build message header
    if start_date == end_date:
        date_range = f"日期: {start_date}"
    else:
        date_range = f"日期范围: {start_date} 至 {end_date}"
    
    message_parts = [
        f"📊 {title}",
        f"{date_range}",
        "",
        "=" * 30,
        ""
    ]
    
    # Total statistics
    total_leads = leads.get('total_leads', 0)
    total_orders = orders.get('total_orders', 0)
    
    message_parts.extend([
        f"📈 总线索数: {total_leads}",
        f"📦 总订单数: {total_orders}",
        ""
    ])
    
    # Leads by sales
    if leads.get('by_sales'):
        message_parts.append("👥 线索分销售统计:")
        for item in leads['by_sales']:
            sales_name = item.get('sales', '未知')
            leads_count = item.get('leads_count', 0)
            message_parts.append(f"  • {sales_name}: {leads_count} 个线索")
        message_parts.append("")
    
    # Orders by sales
    if orders.get('by_sales'):
        message_parts.append("💰 订单分销售统计:")
        for item in orders['by_sales']:
            sales_name = item.get('sales', '未知')
            orders_count = item.get('orders_count', 0)
            total_sales = item.get('total_sales', 0)
            # Display total sales as integer
            try:
                total_sales_int = int(total_sales)
            except Exception:
                total_sales_int = 0
            message_parts.append(f"  • {sales_name}: {orders_count} 个订单, 总额: ¥{total_sales_int}")
        message_parts.append("")
    
    message_parts.append("=" * 30)
    
    return "\n".join(message_parts)


def format_daily_report(stats):
    """
    Format daily report message
    
    Args:
        stats: Statistics dictionary
        
    Returns:
        str: Formatted daily report
    """
    return format_stats_message(stats, "每日数据报告 - 前一日")


def format_today_report(stats):
    """
    Format today's report message
    
    Args:
        stats: Statistics dictionary
        
    Returns:
        str: Formatted today's report
    """
    return format_stats_message(stats, "今日数据报告")


def format_recent_days_report(stats, days):
    """
    Format recent days report message
    
    Args:
        stats: Statistics dictionary
        days: Number of days
        
    Returns:
        str: Formatted recent days report
    """
    return format_stats_message(stats, f"最近{days}日数据报告")
