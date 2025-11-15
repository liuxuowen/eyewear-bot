"""
Main application module for the eyewear bot
"""
from flask import Flask, request, jsonify, make_response
import atexit
from config import FLASK_PORT
from scheduler import start_scheduler
from query_handler import QueryHandler
from wechat_bot import WeChatBot
from wechatpy.enterprise.crypto import WeChatCrypto
from wechatpy.enterprise import parse_message, create_reply
import os


app = Flask(__name__)

# Start the scheduler
scheduler = start_scheduler()

# Initialize query handler
query_handler = QueryHandler()


TOKEN = os.getenv('WECHAT_TOKEN')
AES_KEY = os.getenv('WECHAT_AES_KEY')
CORP_ID = os.getenv('WECHAT_CORP_ID')

crypto = WeChatCrypto(TOKEN, AES_KEY, CORP_ID)

@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    if request.method == 'GET':
        # 企业微信验证URL
        msg_signature = request.args.get('msg_signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')
        try:
            echo = crypto.check_signature(msg_signature, timestamp, nonce, echostr)
            return echo
        except Exception as e:
            return str(e), 400

    # POST: 接收消息
    msg_signature = request.args.get('msg_signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    xml = request.data
    try:
        decrypted_xml = crypto.decrypt_message(xml, msg_signature, timestamp, nonce)
        msg = parse_message(decrypted_xml)
        # 处理消息内容
        if msg.type == 'text':
            reply_content = query_handler.process_query(msg.content)
            reply = create_reply(reply_content, msg)
        else:
            reply = create_reply('不支持非文本命令', msg)
        encrypted_reply = crypto.encrypt_message(reply.render(), nonce, timestamp)
        response = make_response(encrypted_reply)
        response.content_type = 'application/xml'
        return response
    except Exception as e:
        return str(e), 400



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
