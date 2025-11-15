"""
Query handler module for processing user queries
"""
import re
import logging
from datetime import datetime, timedelta
from database import Database
from wechat_bot import WeChatBot
from message_formatter import format_today_report, format_recent_days_report


class QueryHandler:
    """Handler for processing user queries from WeChat"""

    def __init__(self):
        self.db = Database()
        self.bot = WeChatBot()
        # 日志初始化（只初始化一次即可）
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(message)s',
        )
    
    def process_query(self, query_text):
        """
        Process a query from user
        
        Args:
            query_text: Query text from user
            
        Returns:
            str: Response message
        """
        query_text = query_text.strip()
        logging.info(f"收到 query_text: {query_text}")

        # Handle "今日" query
        if query_text == "今日":
            logging.info("分支: 今日查询")
            return self.handle_today_query()

        # Handle "最近n日" query
        match = re.match(r'最近(\d+)日', query_text)
        if match:
            days = int(match.group(1))
            logging.info(f"分支: 最近{days}日查询")
            return self.handle_recent_days_query(days)

        # Unknown query
        logging.info("分支: 未知查询格式")
        return self.handle_unknown_query()
    
    def handle_today_query(self):
        """
        Handle today's data query
        
        Returns:
            str: Formatted today's statistics
        """
        try:
            today = datetime.now().date()
            stats = self.db.get_combined_stats(today, today)
            message = format_today_report(stats)
            return message
        except Exception as e:
            return f"查询今日数据时出错: {str(e)}"
    
    def handle_recent_days_query(self, days):
        """
        Handle recent days data query
        
        Args:
            days: Number of recent days to query
            
        Returns:
            str: Formatted statistics for recent days
        """
        try:
            if days <= 0:
                return "请输入有效的天数（大于0）"
            
            if days > 365:
                return "查询天数不能超过365天"
            
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days-1)
            
            stats = self.db.get_combined_stats(start_date, end_date)
            message = format_recent_days_report(stats, days)
            return message
        except Exception as e:
            return f"查询最近{days}日数据时出错: {str(e)}"
    
    def handle_unknown_query(self):
        """
        Handle unknown query format
        
        Returns:
            str: Help message
        """
        return """❓ 未知查询格式

支持的查询命令:
• 今日 - 查询今日的订单和线索数据
• 最近n日 - 查询最近n天的数据（例如：最近7日）

示例:
@机器人 今日
@机器人 最近7日
@机器人 最近30日"""
