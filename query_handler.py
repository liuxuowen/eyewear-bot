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

        # 今日/今天
        if query_text in ["今日", "今天"]:
            logging.info("分支: 今日/今天查询")
            return self.handle_today_query()

        # 昨日/昨天
        if query_text in ["昨日", "昨天"]:
            logging.info("分支: 昨日/昨天查询")
            return self.handle_yesterday_query()

        # 本月
        if query_text in ["本月"]:
            logging.info("分支: 本月查询")
            return self.handle_this_month_query()

        # 上个月
        if query_text in ["上个月", "上月"]:
            logging.info("分支: 上个月查询")
            return self.handle_last_month_query()

        # 最近n日/最近n天
        match = re.match(r'最近(\d+)(日|天)', query_text)
        if match:
            days = int(match.group(1))
            logging.info(f"分支: 最近{days}{match.group(2)}查询")
            return self.handle_recent_days_query(days, include_date_group=True)

        # Unknown query
        logging.info("分支: 未知查询格式")
        return self.handle_unknown_query()
    
    def handle_this_month_query(self):
        """
        查询本月数据（从当月1号到今天）
        """
        try:
            today = datetime.now().date()
            start_date = today.replace(day=1)
            stats = self.db.get_combined_stats(start_date, today)
            message = format_recent_days_report(stats, (today - start_date).days + 1)
            return message
        except Exception as e:
            logging.error(f"handle_this_month_query 异常: {str(e)}")
            return f"查询本月数据时出错: {str(e)}"

    def handle_last_month_query(self):
        """
        查询上个月数据（从上月1号到上月最后一天）
        """
        try:
            today = datetime.now().date()
            first_day_this_month = today.replace(day=1)
            last_day_last_month = first_day_this_month - timedelta(days=1)
            first_day_last_month = last_day_last_month.replace(day=1)
            stats = self.db.get_combined_stats(first_day_last_month, last_day_last_month)
            message = format_recent_days_report(stats, (last_day_last_month - first_day_last_month).days + 1)
            return message
        except Exception as e:
            logging.error(f"handle_last_month_query 异常: {str(e)}")
            return f"查询上个月数据时出错: {str(e)}"
    
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

    def handle_yesterday_query(self):
        """
        Handle yesterday's data query
        Returns:
            str: Formatted yesterday's statistics
        """
        try:
            yesterday = datetime.now().date() - timedelta(days=1)
            stats = self.db.get_combined_stats(yesterday, yesterday)
            message = format_today_report(stats)
            return message
        except Exception as e:
            return f"查询昨日数据时出错: {str(e)}"
    
    def handle_recent_days_query(self, days, include_date_group=False):
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
            # 增加日期分组（倒序）
            if hasattr(self.db, 'get_stats_by_date'):
                date_stats = self.db.get_stats_by_date(start_date, end_date)
                message += "\n\n📅 按日期分组（倒序）："
                for d in sorted(date_stats.keys(), reverse=True):
                    message += f"\n{d}: {date_stats[d]}"
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
    • 今日/今天 - 查询今日的订单和线索数据
    • 昨日/昨天 - 查询昨日的订单和线索数据
    • 本月 - 查询本月数据
    • 上个月 - 查询上个月数据
    • 最近n日/最近n天 - 查询最近n天的数据（例如：最近7日、最近30天）

    示例:
    @机器人 今日/今天
    @机器人 昨天/昨日
    @机器人 本月
    @机器人 上个月/上月
    @机器人 最近7日
    @机器人 最近30天"""
