"""
LINE Bot handler module
"""
import logging
from typing import Optional
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, ImageMessage, FileMessage

from config import config
from modules.utils.logger import log_error_with_traceback, StructuredLogger


class LineBotHandler:
    """LINE Bot message handler"""
    
    def __init__(self):
        """Initialize LINE Bot handler"""
        self.logger = StructuredLogger(__name__)
        
        # Validate LINE Bot configuration
        if not config.LINE_CHANNEL_ACCESS_TOKEN or not config.LINE_CHANNEL_SECRET:
            raise ValueError("LINE Bot configuration is missing")
        
        # Initialize LINE Bot API
        self.line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)
        self.handler = WebhookHandler(config.LINE_CHANNEL_SECRET)
        
        # Setup Flask app for webhook
        self.app = Flask(__name__)
        self.setup_routes()
        self.setup_handlers()
        
        self.logger.info("LINE Bot handler initialized")
    
    def setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route("/webhook", methods=['POST'])
        def webhook():
            """LINE webhook endpoint"""
            # Get X-Line-Signature header value
            signature = request.headers['X-Line-Signature']
            
            # Get request body as text
            body = request.get_data(as_text=True)
            
            self.logger.info("Received webhook request", 
                           signature=signature[:10] + "...",
                           body_length=len(body))
            
            # Handle webhook body
            try:
                self.handler.handle(body, signature)
            except InvalidSignatureError:
                self.logger.error("Invalid signature")
                abort(400)
            except Exception as e:
                log_error_with_traceback(
                    logging.getLogger(__name__), 
                    "Webhook handling error", 
                    e
                )
                abort(500)
            
            return 'OK'
        
        @self.app.route("/health", methods=['GET'])
        def health():
            """Health check endpoint"""
            return {"status": "ok", "service": "LINE Bot OneDrive AI"}
    
    def setup_handlers(self):
        """Setup LINE Bot message handlers"""
        
        @self.handler.add(MessageEvent, message=TextMessage)
        def handle_text_message(event):
            """Handle text messages"""
            try:
                user_id = event.source.user_id
                message_text = event.message.text
                
                self.logger.info("Received text message", 
                               user_id=user_id, 
                               message=message_text)
                
                # Process text message
                response = self.process_text_message(user_id, message_text)
                
                # Send response
                if response:
                    self.send_text_message(event.reply_token, response)
                
            except Exception as e:
                log_error_with_traceback(
                    logging.getLogger(__name__), 
                    "Text message handling error", 
                    e
                )
                self.send_error_message(event.reply_token)
        
        @self.handler.add(MessageEvent, message=ImageMessage)
        def handle_image_message(event):
            """Handle image messages"""
            try:
                user_id = event.source.user_id
                message_id = event.message.id
                
                self.logger.info("Received image message", 
                               user_id=user_id, 
                               message_id=message_id)
                
                # Process image message
                response = self.process_image_message(user_id, message_id)
                
                # Send response
                if response:
                    self.send_text_message(event.reply_token, response)
                
            except Exception as e:
                log_error_with_traceback(
                    logging.getLogger(__name__), 
                    "Image message handling error", 
                    e
                )
                self.send_error_message(event.reply_token)
        
        @self.handler.add(MessageEvent, message=FileMessage)
        def handle_file_message(event):
            """Handle file messages"""
            try:
                user_id = event.source.user_id
                message_id = event.message.id
                file_name = event.message.fileName
                
                self.logger.info("Received file message", 
                               user_id=user_id, 
                               message_id=message_id,
                               file_name=file_name)
                
                # Process file message
                response = self.process_file_message(user_id, message_id, file_name)
                
                # Send response
                if response:
                    self.send_text_message(event.reply_token, response)
                
            except Exception as e:
                log_error_with_traceback(
                    logging.getLogger(__name__), 
                    "File message handling error", 
                    e
                )
                self.send_error_message(event.reply_token)
    
    def process_text_message(self, user_id: str, message: str) -> Optional[str]:
        """
        Process text message
        
        Args:
            user_id: LINE user ID
            message: Text message content
            
        Returns:
            Response message or None
        """
        # Basic command processing
        message_lower = message.lower().strip()
        
        if message_lower in ['hello', 'hi', 'こんにちは']:
            return "こんにちは！ファイルやレシート画像を送信してください。"
        
        elif message_lower in ['help', 'ヘルプ']:
            return self.get_help_message()
        
        elif message_lower in ['status', 'ステータス']:
            return "システムは正常に動作しています。"
        
        else:
            return "申し訳ございませんが、コマンドが認識できませんでした。'ヘルプ'と送信してください。"
    
    def process_image_message(self, user_id: str, message_id: str) -> Optional[str]:
        """
        Process image message
        
        Args:
            user_id: LINE user ID
            message_id: Message ID
            
        Returns:
            Response message or None
        """
        # TODO: Implement image processing with OneDrive upload and AI analysis
        return "画像を受信しました。処理中です..."
    
    def process_file_message(self, user_id: str, message_id: str, file_name: str) -> Optional[str]:
        """
        Process file message
        
        Args:
            user_id: LINE user ID
            message_id: Message ID
            file_name: Original file name
            
        Returns:
            Response message or None
        """
        # TODO: Implement file processing with OneDrive upload
        return f"ファイル '{file_name}' を受信しました。処理中です..."
    
    def send_text_message(self, reply_token: str, message: str):
        """Send text message"""
        try:
            from linebot.models import TextSendMessage
            self.line_bot_api.reply_message(reply_token, TextSendMessage(text=message))
            
        except LineBotApiError as e:
            log_error_with_traceback(
                logging.getLogger(__name__), 
                "Failed to send message", 
                e
            )
    
    def send_error_message(self, reply_token: str):
        """Send error message"""
        error_msg = "申し訳ございません。処理中にエラーが発生しました。しばらく後に再度お試しください。"
        self.send_text_message(reply_token, error_msg)
    
    def get_help_message(self) -> str:
        """Get help message"""
        return """【使用方法】
📁 ファイルアップロード: ファイルを送信
📸 レシート読取: レシート画像を送信
💰 売上確認: 'ステータス'と送信
❓ ヘルプ: 'ヘルプ'と送信

何かご不明な点がございましたら、管理者にお問い合わせください。"""
    
    def start_server(self, port: int = 8000):
        """Start Flask server"""
        self.logger.info(f"Starting LINE Bot server on port {port}")
        self.app.run(host='0.0.0.0', port=port, debug=config.DEBUG)