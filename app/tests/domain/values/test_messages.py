from datetime import datetime
import pytest

from domain.entities.messages import Chat, Message
from domain.exceptions.messages import TitleTooLongException
from domain.values.messages import Text, Title


def test_create_message_success_short_text():
    text = Text('test message success')
    message = Message(text=text)
    
    assert message.text == text
    assert message.created_at.date() == datetime.today().date()
    
    
def test_create_message_sucess_long_text():
    text = Text('a' * 400)
    message = Message(text=text)
        
    assert message.text == text
    assert message.created_at.date() == datetime.today().date()
    

def test_create_chat_success():
    title = Title('title success')
    chat = Chat(title=title)
    
    assert chat.title == title
    assert not chat.messages
    assert chat.created_at.date() == datetime.today().date()
    

def test_create_chat_title_too_long():
    with pytest.raises(TitleTooLongException):
        Title('a' * 400)

def test_add_chat_to_message():
    text = Text('test message success')
    message = Message(text=text)
    
    title = Title('title success')
    chat = Chat(title=title)
    
    chat.add_message(message)
    
    assert message in chat.messages