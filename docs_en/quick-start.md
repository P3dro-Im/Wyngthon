---
hide:
  - navigation
---

# Quick Start

A quick guide to getting started with Wyngthon. In this section you will learn how to create your first client and perform basic operations.

---

## Creating a Client

### Simple method (without API ID and Hash)

Wyngthon ships with default API credentials for Wyng, so you can create a client without obtaining your own keys:

```python
from wyngthon import WyngClient, events, sync
from wyngthon.sessions import StringSession

# No api_id or api_hash needed
client = WyngClient(StringSession())
client.start()
```

### Standard method (with API ID and Hash)

For standard usage, you first need to obtain your API ID and Hash from [my.telegram.org](https://my.telegram.org/):

```python
from wyngthon import WyngClient

api_id = 12345
api_hash = '0123456789abcdef0123456789abcdef'

# The first parameter is the session file name
with WyngClient('anon', api_id, api_hash) as client:
    client.loop.run_until_complete(client.send_message('me', 'Hello, myself!'))
```

!!! important "Important"
    Avoid naming your script `wyngthon.py`! Python will try to import the client from that file and fail with an error.

---

## Sending Messages

### Send to yourself

```python
await client.send_message('me', 'Hello, myself!')
```

### Send to a chat by ID

```python
await client.send_message(-100123456, 'Hello, group!')
```

### Send to a contact

```python
await client.send_message('+989123456789', 'Hello, my friend!')
```

### Send to a username

```python
await client.send_message('username', 'Testing Wyngthon!')
```

### Send with formatting

```python
message = await client.send_message(
    'me',
    'This message has **bold**, `code`, __italic__ and '
    'a [beautiful website](https://example.com)!',
    link_preview=False
)

# Print the raw text of the message
print(message.raw_text)
```

---

## Getting User Information

```python
# Get your own information
me = await client.get_me()

# Display the information as a string
print(me.stringify())

# Access attributes
username = me.username
print(username)
print(me.phone)
```

---

## Printing Conversations

```python
async for dialog in client.iter_dialogs():
    print(dialog.name, 'has ID', dialog.id)
```

---

## Replying to Messages

```python
# If you have a message object, you can reply to it directly
await message.reply('Great!')
```

---

## Sending Files

```python
await client.send_file('me', '/home/me/Pictures/holidays.jpg')
```

---

## Printing Message History

```python
async for message in client.iter_messages('me'):
    print(message.id, message.text)
    
    # Download media from messages
    if message.photo:
        path = await message.download_media()
        print('File saved to', path)
```

---

## Complete Example

Here is a complete quick-start example:

```python
from wyngthon import WyngClient

api_id = 12345
api_hash = '0123456789abcdef0123456789abcdef'
client = WyngClient('anon', api_id, api_hash)

async def main():
    # Get your own information
    me = await client.get_me()
    print(me.stringify())
    
    # Username
    username = me.username
    print(username)
    print(me.phone)
    
    # Print all conversations
    async for dialog in client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)
    
    # Send a message to yourself
    await client.send_message('me', 'Hello, myself!')
    
    # Send a message to a chat
    await client.send_message(-100123456, 'Hello, group!')
    
    # Send a message to a contact
    await client.send_message('+989123456789', 'Hello, my friend!')
    
    # Send a message to a username
    await client.send_message('username', 'Testing Wyngthon!')
    
    # Send with formatting
    message = await client.send_message(
        'me',
        'This message has **bold**, `code`, __italic__ and '
        'a [beautiful website](https://example.com)!',
        link_preview=False
    )
    
    print(message.raw_text)
    await message.reply('Great!')
    
    # Send a file
    await client.send_file('me', '/home/me/Pictures/holidays.jpg')
    
    # Print message history
    async for message in client.iter_messages('me'):
        print(message.id, message.text)
        
        if message.photo:
            path = await message.download_media()
            print('File saved to', path)

with client:
    client.loop.run_until_complete(main())
```

---

## Important Notes

!!! tip "Tip"
    Wyngthon is an asynchronous (async) library, so you need to work with asyncio. In general, write all of your code inside an `async def` function:

```python
client = ...

async def do_something(me):
    ...

async def main():
    # Most of your code should go here
    me = await client.get_me()
    await do_something(me)

with client:
    client.loop.run_until_complete(main())
```

---

## Next Step

Once you are familiar with the basics, head over to [Core Concepts](concepts/index.md) to better understand important concepts such as Entity, Session and events.
