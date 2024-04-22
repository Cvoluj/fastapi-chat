from datetime import datetime
import pytest

from domain.entities.messages import Chat, Message
from domain.exceptions.messages import TitleTooLongException
from domain.values.messages import Text, Title
from domain.events.messages import NewMessageRecievedEvent

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

def test_new_message_event():
    text = Text('Hello World')
    message = Message(text=text)
    
    title = Title('title')
    chat = Chat(title=title)
    
    chat.add_message(message)
    events = chat.pull_events()
    pulled_events = chat.pull_events()
    
    assert not pulled_events
    assert len(events) == 1, events
    
    new_event = events[0]
    
    assert isinstance(new_event, NewMessageRecievedEvent), new_event
    assert new_event.message_oid == message.oid
    assert new_event.message_text == message.text.as_generic_type()
    assert new_event.chat_oid == chat.oid
