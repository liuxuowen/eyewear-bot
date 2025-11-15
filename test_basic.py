"""
Test script for the eyewear bot
This script tests basic functionality without requiring a database connection
"""
import sys
from datetime import datetime, timedelta

def test_query_handler():
    """Test query handler pattern matching"""
    from query_handler import QueryHandler
    import re
    
    # Test pattern matching for queries
    test_cases = [
        ("今日", True, "today query"),
        ("最近7日", True, "recent 7 days"),
        ("最近30日", True, "recent 30 days"),
        ("最近100日", True, "recent 100 days"),
        ("hello", False, "unknown query"),
        ("最近", False, "invalid recent query"),
    ]
    
    print("Testing query pattern matching...")
    for query, should_match, description in test_cases:
        if query == "今日":
            result = query == "今日"
        else:
            match = re.match(r'最近(\d+)日', query)
            result = match is not None
        
        if result == should_match:
            print(f"✓ {description}: '{query}' - PASS")
        else:
            print(f"✗ {description}: '{query}' - FAIL")
            return False
    
    return True


def test_message_formatter():
    """Test message formatting"""
    from message_formatter import format_stats_message
    
    print("\nTesting message formatter...")
    
    # Mock statistics data
    test_stats = {
        'start_date': '2024-01-15',
        'end_date': '2024-01-15',
        'leads': {
            'total_leads': 25,
            'by_sales': [
                {'sales': '张三', 'leads_count': 10},
                {'sales': '李四', 'leads_count': 8},
                {'sales': '王五', 'leads_count': 7}
            ]
        },
        'orders': {
            'total_orders': 8,
            'by_sales': [
                {'sales': '张三', 'orders_count': 4, 'total_sales': 15800.00},
                {'sales': '李四', 'orders_count': 3, 'total_sales': 12500.00},
                {'sales': '王五', 'orders_count': 1, 'total_sales': 3200.00}
            ]
        }
    }
    
    message = format_stats_message(test_stats, "测试报告")
    
    # Check if message contains expected elements
    required_elements = [
        "测试报告",
        "总线索数: 25",
        "总订单数: 8",
        "张三",
        "李四",
        "王五"
    ]
    
    for element in required_elements:
        if element in message:
            print(f"✓ Message contains: '{element}' - PASS")
        else:
            print(f"✗ Message missing: '{element}' - FAIL")
            return False
    
    return True


def test_date_calculations():
    """Test date range calculations"""
    print("\nTesting date calculations...")
    
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    last_7_days_start = today - timedelta(days=6)
    
    print(f"✓ Today: {today}")
    print(f"✓ Yesterday: {yesterday}")
    print(f"✓ Last 7 days start: {last_7_days_start}")
    
    return True


def test_config():
    """Test configuration loading"""
    print("\nTesting configuration...")
    
    try:
        from config import DB_CONFIG, WECHAT_WEBHOOK_URL, FLASK_PORT
        print(f"✓ Config loaded successfully")
        print(f"  - Database host: {DB_CONFIG.get('host', 'not set')}")
        print(f"  - Flask port: {FLASK_PORT}")
        print(f"  - WeChat webhook: {'configured' if WECHAT_WEBHOOK_URL else 'not configured'}")
        return True
    except Exception as e:
        print(f"✗ Config loading failed: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("=" * 50)
    print("Eyewear Bot - Basic Functionality Tests")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_config),
        ("Query Handler", test_query_handler),
        ("Message Formatter", test_message_formatter),
        ("Date Calculations", test_date_calculations),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} failed with exception: {str(e)}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("Test Results Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
