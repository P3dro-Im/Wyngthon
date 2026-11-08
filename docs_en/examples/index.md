---
hide:
  - navigation
---

# Examples

This section contains practical, hands-on examples to help you learn Wyngthon.

---

## Table of Contents

<div class="grid cards" markdown>

-   :material-account:{ .lg .middle } __Users__

    ---

    Examples for working with users in Wyngthon.

    [:octicons-arrow-right-24: View](users.md)

-   :material-chat:{ .lg .middle } __Chats and Channels__

    ---

    Examples for working with chats and channels.

    [:octicons-arrow-right-24: View](chats-and-channels.md)

-   :material-message:{ .lg .middle } __Working with Messages__

    ---

    Examples for working with messages.

    [:octicons-arrow-right-24: View](working-with-messages.md)

-   :material-alert:{ .lg .middle } __Word of Warning__

    ---

    Important notes and warnings when using Wyngthon.

    [:octicons-arrow-right-24: View](word-of-warning.md)

</div>

---

## Simple Examples

### Sending a Simple Message

```python
from wyngthon import WyngClient

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        await client.send_message('me', 'Hello, myself!')
        
        # Send with formatting
        await client.send_message('me', 'This message is **bold**.')
        
        # Send with link preview disabled
        await client.send_message('me', 'https://example.com', link_preview=False)

import asyncio
asyncio.run(main())
```

### Receiving Messages

```python
from wyngthon import WyngClient

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Get the latest messages
        messages = await client.get_messages('me', limit=10)
        
        for message in messages:
            print(f'{message.id}: {message.text}')

import asyncio
asyncio.run(main())
```

### Sending Files

```python
from wyngthon import WyngClient

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Send a photo
        await client.send_file('me', '/path/to/photo.jpg')
        
        # Send a file with a caption
        await client.send_file('me', '/path/to/file.pdf', caption='Important file')

import asyncio
asyncio.run(main())
```

---

## Event Examples

### Auto-Replying to Messages

```python
from wyngthon import WyngClient, events

client = WyngClient('anon', api_id, api_hash)

@client.on(events.NewMessage(pattern=r'(?i)hi|hello'))
async def handler(event):
    await event.reply('Hello! How can I help?')

@client.on(events.NewMessage(pattern=r'(?i)help'))
async def help_handler(event):
    await event.respond('This is a help message.')

client.start()
client.run_until_disconnected()
```

### Replying to a Specific Message

```python
from wyngthon import WyngClient, events

client = WyngClient('anon', api_id, api_hash)

@client.on(events.NewMessage(outgoing=True, pattern=r'\.save'))
async def handler(event):
    if event.is_reply:
        replied = await event.get_reply_message()
        sender = replied.sender
        await client.download_profile_photo(sender)
        await event.respond(f'Your photo has been saved {sender.username}')

client.start()
client.run_until_disconnected()
```

---

## Advanced Examples

### Error Handling

```python
from wyngthon import WyngClient, events
from wyngthon.errors import FloodWaitError, RPCError

client = WyngClient('anon', api_id, api_hash)

async def safe_send(client, entity, message):
    try:
        await client.send_message(entity, message)
        return True
    except FloodWaitError as e:
        import asyncio
        await asyncio.sleep(e.seconds)
        return True
    except RPCError as e:
        print(f'Error: {e}')
        return False

@client.on(events.NewMessage)
async def handler(event):
    await safe_send(client, 'me', 'Automatic reply')

client.start()
client.run_until_disconnected()
```

### Working with Multiple Clients

```python
import asyncio
from wyngthon import WyngClient

async def run_client(name, api_id, api_hash):
    client = WyngClient(name, api_id, api_hash)
    await client.start()
    print(f'Client {name} started')
    await client.run_until_disconnected()

async def main():
    await asyncio.gather(
        run_client('client1', api_id1, api_hash1),
        run_client('client2', api_id2, api_hash2)
    )

asyncio.run(main())
```

---

## Important Notes

!!! note "Note"
    These examples assume that you have obtained your API ID and Hash from [my.telegram.org](https://my.telegram.org/).

---

## Next Steps

To learn more, read the following sections:

- [API Reference](../api-reference.md): Complete API documentation
- [FAQ](../faq.md): Answers to common questions
