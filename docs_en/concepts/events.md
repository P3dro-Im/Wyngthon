---
hide:
  - navigation
---

# Events

Events are an important topic in a messaging platform like Wyng. Ultimately, you want to be notified when a new message arrives, a new member joins, someone is typing, and so on. You can use **events** for this.

---

## Getting Started

Let's start with an example of an automatic reply:

```python
from wyngthon import WyngClient, events

client = WyngClient('anon', api_id, api_hash)

@client.on(events.NewMessage)
async def my_event_handler(event):
    if 'hello' in event.raw_text:
        await event.reply('hi!')

client.start()
client.run_until_disconnected()
```

This isn't much code, but some of it may be unclear. Let's break it down:

### Creating the client

```python
from wyngthon import WyngClient, events

client = WyngClient('anon', api_id, api_hash)
```

Creation is the usual (passing the session name, API ID and hash, of course). Nothing we don't already know.

### The event decorator

```python
@client.on(events.NewMessage)
```

This Python decorator attaches itself to the `my_event_handler` definition, and essentially means that *on* a `NewMessage` event, the callback function you are about to define will be called:

### The event handler

```python
async def my_event_handler(event):
    if 'hello' in event.raw_text:
        await event.reply('hi!')
```

If a `NewMessage` event occurs and `'hello'` is in the message text, we reply to the event with the message `'hi!'`.

!!! note "Note"
    Event handlers **must** be `async def`. After all, Wyngthon is an asynchronous library built on asyncio, an approach that is safer and often faster than threads.
>
> You **must** `await` every method call that uses a network request, which is most of them.

---

## Main Event Types

### NewMessage

When a new message is received:

```python
@client.on(events.NewMessage)
async def handler(event):
    print(event.raw_text)
```

### NewMessage with filters

Filtering outgoing messages:

```python
@client.on(events.NewMessage(outgoing=True))
async def handler(event):
    # Only messages you have sent
    print(event.raw_text)
```

Filtering with regex:

```python
@client.on(events.NewMessage(pattern=r'\.save'))
async def handler(event):
    # Only messages that start with ".save"
    if event.is_reply:
        replied = await event.get_reply_message()
        sender = replied.sender
        await client.download_profile_photo(sender)
        await event.respond('Your photo was saved {}'.format(sender.username))
```

### MessageEdited

When a message is edited:

```python
@client.on(events.MessageEdited)
async def handler(event):
    print('Message edited:', event.raw_text)
```

### MessageDeleted

When a message is deleted:

```python
@client.on(events.MessageDeleted)
async def handler(event):
    print('Message deleted:', event.message_id)
```

### CallbackQuery

When an inline button is clicked:

```python
@client.on(events.CallbackQuery)
async def handler(event):
    print('Button clicked:', event.data)
    await event.answer('You clicked the button!')
```

### ChatAction

When a new member joins or leaves the chat:

```python
@client.on(events.ChatAction)
async def handler(event):
    if event.user_joined:
        print('New member joined:', event.user_id)
    if event.user_left:
        print('Member left:', event.user_id)
```

### InlineQuery

When an inline query is received:

```python
@client.on(events.InlineQuery)
async def handler(event):
    # Answer the inline query
    await event.answer([
        event.builder.article('Result 1', text='Text of result 1')
    ])
```

### UserUpdate

When user information changes:

```python
@client.on(events.UserUpdate)
async def handler(event):
    print('User updated:', event.status)
```

---

## More Examples

### Deleting messages that contain a specific word

Let's delete messages containing "heck". No swearing allowed here:

```python
@client.on(events.NewMessage(pattern=r'(?i).*heck'))
async def handler(event):
    await event.delete()
```

With the regex `r'(?i).*heck'`, we match "heck" case-insensitively anywhere in the message. Regex is very powerful, and you can learn more at https://regexone.com/.

### Replying to a specific message

```python
@client.on(events.NewMessage(pattern=r'(?i)hi|hello'))
async def handler(event):
    await event.respond('Hello! How can I help?')
```

### Listening to a specific channel

```python
@client.on(events.NewMessage(chats='channel_username'))
async def handler(event):
    # Only messages from a specific channel
    print(event.raw_text)
```

### Filtering outgoing and incoming messages

```python
# Only outgoing messages (messages you have sent)
@client.on(events.NewMessage(outgoing=True))
async def handler_outgoing(event):
    print('You sent:', event.raw_text)

# Only incoming messages (messages sent by others)
@client.on(events.NewMessage(incoming=True))
async def handler_incoming(event):
    print('You received:', event.raw_text)
```

---

## Accessing Entities in Events

When you need the user or chat in which the event occurred, you **must** use the following methods:

```python
async def handler(event):
    # Correct
    chat = await event.get_chat()
    sender = await event.get_sender()
    chat_id = event.chat_id
    sender_id = event.sender_id
    
    # Wrong - don't do this
    chat = event.chat
    sender = event.sender
    chat_id = event.chat.id
    sender_id = event.sender.id
```

Events are like messages, but they don't have all of a message's information! When you fetch a message manually, it has all the necessary information. But when you receive an update about a message, it **doesn't have all the information**, so you must use **methods**, not properties.

---

## Important Notes

!!! important "Important"
    Don't forget to enable logging when working with events, because errors in event handlers are hidden by default. Please add the following snippet at the top of your file:

```python
import logging
logging.basicConfig(format='[%(levelname) %(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
```

---

## Summary

Events let you respond to various messages and happenings on Wyng. Using the `@client.on()` decorators, you can register different handlers for different event types.

---

## Next Step

To learn more about String Sessions, read the [String Sessions](string-sessions.md) section.
