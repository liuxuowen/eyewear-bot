"""
WeChat Work Bot messaging module
"""
import requests
import json
from config import WECHAT_WEBHOOK_URL


class WeChatBot:
    """WeChat Work Bot for sending messages"""
    
    def __init__(self, webhook_url=None):
        self.webhook_url = webhook_url or WECHAT_WEBHOOK_URL
    
    def send_text_message(self, content):
        """
        Send a text message through WeChat Work Bot
        
        Args:
            content: Message content to send
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.webhook_url:
            print("Warning: WeChat webhook URL not configured")
            return False
        
        data = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                data=json.dumps(data),
                headers={'Content-Type': 'application/json'}
            )
            result = response.json()
            
            if result.get('errcode') == 0:
                print(f"Message sent successfully: {content[:50]}...")
                return True
            else:
                print(f"Failed to send message: {result}")
                return False
        except Exception as e:
            print(f"Error sending message: {str(e)}")
            return False
    
    def send_markdown_message(self, content):
        """
        Send a markdown message through WeChat Work Bot
        
        Args:
            content: Markdown content to send
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.webhook_url:
            print("Warning: WeChat webhook URL not configured")
            return False
        
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": content
            }
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                data=json.dumps(data),
                headers={'Content-Type': 'application/json'}
            )
            result = response.json()
            
            if result.get('errcode') == 0:
                print(f"Markdown message sent successfully")
                return True
            else:
                print(f"Failed to send markdown message: {result}")
                return False
        except Exception as e:
            print(f"Error sending markdown message: {str(e)}")
            return False
