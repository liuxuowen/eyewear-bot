"""
Main application module for the eyewear bot
"""
from flask import Flask, request, jsonify
import atexit
from config import FLASK_PORT
from scheduler import start_scheduler
from query_handler import QueryHandler
from wechat_bot import WeChatBot

app = Flask(__name__)

# Start the scheduler
scheduler = start_scheduler()

# Initialize query handler
query_handler = QueryHandler()


@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Webhook endpoint for receiving messages from WeChat Work Bot
    
    Expected JSON payload:
    {
        "msgtype": "text",
        "text": {
            "content": "query text"
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Extract message content
        msgtype = data.get('msgtype', '')
        
        if msgtype == 'text':
            content = data.get('text', {}).get('content', '')
            
            # Process the query
            response = query_handler.process_query(content)
            
            # Send response
            bot = WeChatBot()
            bot.send_text_message(response)
            
            return jsonify({"status": "success", "message": "Query processed"}), 200
        else:
            return jsonify({"status": "ignored", "message": "Non-text message"}), 200
            
    except Exception as e:
        print(f"Error in webhook: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "scheduler_running": scheduler.running
    }), 200


@app.route('/trigger_daily_report', methods=['POST'])
def trigger_daily_report():
    """
    Manual trigger endpoint for daily report (for testing)
    """
    try:
        from scheduler import daily_report_job
        daily_report_job()
        return jsonify({"status": "success", "message": "Daily report triggered"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def shutdown_scheduler():
    """Shutdown the scheduler gracefully"""
    if scheduler.running:
        scheduler.shutdown()
        print("Scheduler shut down")


# Register shutdown handler
atexit.register(shutdown_scheduler)


if __name__ == '__main__':
    print(f"Starting eyewear bot on port {FLASK_PORT}")
    app.run(host='0.0.0.0', port=FLASK_PORT, debug=False)
