"""
텔레그램 메시지 수집기
"""
IMPORT telethon, asyncio, django_setup
FROM message_parser IMPORT BigSignalParser

CLASS TelegramCollector:
    INITIALIZE:
        - api_id = GET from environment
        - api_hash = GET from environment  
        - phone = GET from environment
        - channel_id = BigSignal 채널 ID
        - parser = BigSignalParser()
        - client = TelegramClient()
    
    METHOD start_collection():
        CONNECT to Telegram
        AUTHENTICATE with phone number
        LISTEN to channel messages
    
    ASYNC METHOD handle_new_message(event):
        message_text = event.message.message
        message_datetime = event.message.date
        
        parsed_trade = parser.parse_message(message_text, message_datetime)
        
        IF parsed_trade:
            SAVE parsed_trade to database
            LOG successful parsing
            TRIGGER portfolio update
        ELSE:
            LOG parsing failure with message content
    
    METHOD run():
        TRY:
            START event loop
            KEEP running until interrupted
        EXCEPT KeyboardInterrupt:
            LOG shutdown message
            CLEANUP connections