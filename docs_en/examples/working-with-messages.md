---
hide:
  - navigation
---

# Working with Messages

This section contains examples for working with messages in Wyngthon.

---

## Sending Text Messages

### Sending to Yourself

```python
from wyngthon import WyngClient

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Send to yourself
        await client.send_message('me', 'Hello, me!')
        
        # Send with formatting
        await client.send_message('me', 'This message is **bold**, `code` and __italic__.')

import asyncio
asyncio.run(main())
```

### Sending to a Username

```python
from wyngthon import WyngClient

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Send to a username
        await client.send_message('username', 'Hello from Wyngthon!')

import asyncio
asyncio.run(main())
```

### Sending to a Phone Number

```python
from wyngthon import WyngClient

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Send to a phone number (must be in your contact list)
        await client.send_message('+989123456789', 'Hello my friend!')

import asyncio
asyncio.run(main())
```

### Sending to a Chat ID

```python
from wyngthon import WyngClient

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Send to a chat ID
        await client.send_message(-100123456, 'Hello group!')

import asyncio
asyncio.run(main())
```

---

## Sending Files

### Sending a Photo

```python
from wyngthon import WyngClient

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Send a photo
        await client.send_file('me', '/path/to/photo.jpg')
        
        # Send a photo with a caption
        await client.send_file('me', '/path/to/photo.jpg', caption='This is a photo.')

import asyncio
asyncio.run(main())
```

### Sending a File

```python
from wyngthon import WyngClient

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Send a file
        await client.send_file('me', '/path/to/file.pdf')
        
        # Send a file with a caption
        await client.send_file('me', '/path/to/file.pdf', caption='Important file')

import asyncio
asyncio.run(main())
```

### Sending a Video

```python
from wyngthon import WyngClient

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Send a video
        await client.send_file('me', '/path/to/video.mp4')
        
        # Send a video with a caption
        await client.send_file('me', '/path/to/video.mp4', caption='Tutorial video')

import asyncio
asyncio.run(main())
```

---

## Receiving Messages

### Getting the Latest Messages

```python
from wyngthon import WyngClient

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Get the last 10 messages
        messages = await client.get_messages('me', limit=10)
        
        for message in messages:
            print(f'{message.id}: {message.text}')

import asyncio
asyncio.run(main())
```

### Getting Specific Messages

```python
from wyngthon import WyngClient

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Get a message by ID
        message = await client.get_messages('me', ids=123)
        print(f'Message: {message.text}')
        
        # Get several messages by their IDs
        messages = await client.get_messages('me', ids=[123, 456, 789])
        for message in messages:
            print(f'{message.id}: {message.text}')

import asyncio
asyncio.run(main())
```

### Searching Messages

```python
from wyngthon import WyngClient

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Search messages
        messages = await client.get_messages('me', search='search term')
        
        for message in messages:
            print(f'{message.id}: {message.text}')

import asyncio
asyncio.run(main())
```

---

## Editing and Deleting Messages

### Editing a Message

```python
from wyngthon import WyngClient

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Send a message
        message = await client.send_message('me', 'Original message')
        
        # Edit the message
        await client.edit_message(message, 'Edited message')

import asyncio
asyncio.run(main())
```

### Deleting a Message

```python
from wyngthon import WyngClient

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Send a message
        message = await client.send_message('me', 'Message to delete')
        
        # Delete the message
        await client.delete_messages([message.id])
        
        # Delete messages by ID
        await client.delete_messages([123, 456])

import asyncio
asyncio.run(main())
```

---

## Replying to Messages

### Direct Reply

```python
from wyngthon import WyngClient

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Get a message
        message = await client.get_messages('me', ids=123)
        
        # Reply to the message
        await message.reply('This is a reply!')

import asyncio
asyncio.run(main())
```

### Replying Using an Event

```python
from wyngthon import WyngClient, events

client = WyngClient('anon', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    # Reply to the message
    await event.reply('Automatic reply!')
    
    # Send a message without replying
    await event.respond('This is a separate message.')

client.start()
client.run_until_disconnected()
```

---

## Downloading Media

### Downloading a Photo

```python
from wyngthon import WyngClient

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Get messages
        messages = await client.get_messages('me', limit=10)
        
        for message in messages:
            if message.photo:
                # Download the photo
                path = await message.download_media()
                print(f'Photo saved: {path}')

import asyncio
asyncio.run(main())
```

### Downloading a File

```python
from wyngthon import WyngClient

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Get messages
        messages = await client.get_messages('me', limit=10)
        
        for message in messages:
            if message.document:
                # Download the file
                path = await message.download_media()
                print(f'File saved: {path}')

import asyncio
asyncio.run(main())
```

---

## Important Notes

!!! note "Note"
    - Use `send_file` to send files
    - Use `download_media` to download media
    - Use `edit_message` to edit a message
    - Use `delete_messages` to delete a message

---

## Next Steps

To learn more, read the [Word of Warning](word-of-warning.md) section.
