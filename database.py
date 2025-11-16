"""
Database operations module
"""
import pymysql
from datetime import datetime, timedelta
from config import DB_CONFIG


class Database:
    """Database connection and query handler"""
    
    def __init__(self):
        self.config = DB_CONFIG
    
    def get_connection(self):
        """Create and return a database connection"""
        return pymysql.connect(**self.config)
    
    def get_leads_stats(self, start_date, end_date):
        """
        Get leads statistics for a date range
        
        Args:
            start_date: Start date (inclusive)
            end_date: End date (inclusive)
            
        Returns:
            dict: Statistics including total leads and breakdown by sales
        """
        conn = self.get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                # Total leads count
                sql_total = """
                    SELECT COUNT(*) as total_leads
                    FROM leads
                    WHERE leads_date >= %s AND leads_date <= %s
                """
                cursor.execute(sql_total, (start_date, end_date))
                total_result = cursor.fetchone()
                
                # Leads by sales person
                sql_by_sales = """
                    SELECT sales, COUNT(*) as leads_count
                    FROM leads
                    WHERE leads_date >= %s AND leads_date <= %s
                    GROUP BY sales
                    ORDER BY leads_count DESC
                """
                cursor.execute(sql_by_sales, (start_date, end_date))
                by_sales_result = cursor.fetchall()
                # Ensure total_sales is integer
                for row in by_sales_result:
                    if 'total_sales' in row:
                        row['total_sales'] = int(row['total_sales'] or 0)
                
                return {
                    'total_leads': total_result['total_leads'] if total_result else 0,
                    'by_sales': by_sales_result
                }
        finally:
            conn.close()
    
    def get_orders_stats(self, start_date, end_date):
        """
        Get sales orders statistics for a date range
        
        Args:
            start_date: Start date (inclusive)
            end_date: End date (inclusive)
            
        Returns:
            dict: Statistics including total orders and breakdown by sales
        """
        conn = self.get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                # Total orders count
                sql_total = """
                    SELECT COUNT(*) as total_orders
                    FROM sales_orders
                    WHERE order_date >= %s AND order_date <= %s
                """
                cursor.execute(sql_total, (start_date, end_date))
                total_result = cursor.fetchone()
                
                # Orders by sales person (joined with leads table)
                sql_by_sales = """
                    SELECT so.sales, COUNT(*) as orders_count, SUM(so.sales_price) as total_sales
                    FROM sales_orders so
                    WHERE so.order_date >= %s AND so.order_date <= %s
                    GROUP BY so.sales
                    ORDER BY orders_count DESC
                """
                cursor.execute(sql_by_sales, (start_date, end_date))
                by_sales_result = cursor.fetchall()
                
                return {
                    'total_orders': total_result['total_orders'] if total_result else 0,
                    'by_sales': by_sales_result
                }
        finally:
            conn.close()
    
    def get_combined_stats(self, start_date, end_date):
        """
        Get combined leads and orders statistics for a date range
        
        Args:
            start_date: Start date (inclusive)
            end_date: End date (inclusive)
            
        Returns:
            dict: Combined statistics
        """
        leads_stats = self.get_leads_stats(start_date, end_date)
        orders_stats = self.get_orders_stats(start_date, end_date)
        
        return {
            'leads': leads_stats,
            'orders': orders_stats,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d')
        }

    def get_stats_by_date(self, start_date, end_date):
        """
        Get aggregated stats grouped by date between start_date and end_date.

        Returns a dict mapping 'YYYY-MM-DD' -> summary string or dict.
        """
        conn = self.get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                # Leads per day
                sql_leads = """
                    SELECT DATE(leads_date) as day, COUNT(*) as leads_count
                    FROM leads
                    WHERE leads_date >= %s AND leads_date <= %s
                    GROUP BY day
                """
                cursor.execute(sql_leads, (start_date, end_date))
                leads_by_day = {row['day'].strftime('%Y-%m-%d'): row['leads_count'] for row in cursor.fetchall()}

                # Orders per day and total sales
                sql_orders = """
                    SELECT DATE(order_date) as day, COUNT(*) as orders_count, SUM(sales_price) as total_sales
                    FROM sales_orders
                    WHERE order_date >= %s AND order_date <= %s
                    GROUP BY day
                """
                cursor.execute(sql_orders, (start_date, end_date))
                orders_by_day = {row['day'].strftime('%Y-%m-%d'): {'orders_count': row['orders_count'], 'total_sales': int(row['total_sales'] or 0)} for row in cursor.fetchall()}

                # Merge results
                days = set(list(leads_by_day.keys()) + list(orders_by_day.keys()))
                result = {}
                for d in days:
                    leads_cnt = leads_by_day.get(d, 0)
                    orders_info = orders_by_day.get(d, {'orders_count': 0, 'total_sales': 0.0})
                    result[d] = f"线索:{leads_cnt} 订单:{orders_info['orders_count']} 销售额:¥{orders_info['total_sales']}"

                return result
        finally:
            conn.close()
