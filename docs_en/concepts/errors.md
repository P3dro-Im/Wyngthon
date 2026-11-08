---
hide:
  - navigation
---

# Error Handling

Wyngthon has a powerful error handling system that lets you handle the various errors of the Wyng API.

---

## Main Errors

### RPCError

These are the main errors of the Wyng API. They occur when your request runs into a problem.

```python
from wyngthon.errors import RPCError, FloodWaitError, PeerFloodError

try:
    await client.send_message('username', 'Hello!')
except FloodWaitError as e:
    # Wait until the wait time is over
    print(f'Wait {e.seconds} seconds')
except PeerFloodError:
    # Message rate limit
    print('You have reached the message sending limit')
except RPCError as e:
    # Other API errors
    print(f'API error: {e}')
```

---

## Common Error Types

### FloodWaitError

When you send requests too quickly and have to wait:

```python
from wyngthon.errors import FloodWaitError

try:
    await client.send_message('username', 'Hello!')
except FloodWaitError as e:
    print(f'Wait {e.seconds} seconds')
    # The library waits automatically
    # or you can wait manually
    import asyncio
    await asyncio.sleep(e.seconds)
```

### PeerFloodError

When you have reached the message sending limit:

```python
from wyngthon.errors import PeerFloodError

try:
    await client.send_message('username', 'Hello!')
except PeerFloodError:
    print('You have reached the message sending limit. Please wait.')
```

### UserBannedInChannelError

When your account is banned in a channel:

```python
from wyngthon.errors import UserBannedInChannelError

try:
    await client.send_message('channel', 'Hello!')
except UserBannedInChannelError:
    print('Your account is banned in this channel.')
```

### ChatWriteForbiddenError

When you don't have permission to write in the chat:

```python
from wyngthon.errors import ChatWriteForbiddenError

try:
    await client.send_message('chat', 'Hello!')
except ChatWriteForbiddenError:
    print('You are not allowed to write in this chat.')
```

### UsernameNotOccupiedError

When the username doesn't exist:

```python
from wyngthon.errors import UsernameNotOccupiedError

try:
    await client.send_message('nonexistent_username', 'Hello!')
except UsernameNotOccupiedError:
    print('The username does not exist.')
```

### UsernameInvalidError

When the username is invalid:

```python
from wyngthon.errors import UsernameInvalidError

try:
    await client.send_message('invalid username!', 'Hello!')
except UsernameInvalidError:
    print('The username is invalid.')
```

---

## Handling General Errors

### Using a general try/except

```python
from wyngthon.errors import RPCError

async def safe_send_message(client, entity, message):
    try:
        await client.send_message(entity, message)
        return True
    except RPCError as e:
        print(f'Error sending message: {e}')
        return False
    except Exception as e:
        print(f'Unexpected error: {e}')
        return False
```

### Creating a decorator for error handling

```python
from functools import wraps
from wyngthon.errors import RPCError

def handle_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except RPCError as e:
            print(f'RPC error: {e}')
            return None
        except Exception as e:
            print(f'Unexpected error: {e}')
            return None
    return wrapper

@handle_errors
async def send_message(client, entity, message):
    await client.send_message(entity, message)
```

---

## Registering Error Handlers

### Using on_error

```python
from wyngthon import WyngClient, events

client = WyngClient('anon', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    await event.reply('Automatic reply')

# Handling errors in handlers
@client.on(events.NewMessage)
async def error_handler(event):
    try:
        # Risky operation
        await event.reply('Reply')
    except Exception as e:
        print(f'Error in handler: {e}')
```

---

## Logging Errors

### Using logging

```python
import logging
from wyngthon import WyngClient, events

# Configure logging
logging.basicConfig(
    format='[%(levelname) %(asctime)s] %(name)s: %(message)s',
    level=logging.WARNING
)

client = WyngClient('anon', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    try:
        await event.reply('Reply')
    except Exception as e:
        logging.error(f'Error in handler: {e}')
        raise  # Re-raise the error so it gets logged
```

---

## Practical Examples

### Sending a message with error handling

```python
from wyngthon import WyngClient, events
from wyngthon.errors import FloodWaitError, PeerFloodError, RPCError

client = WyngClient('anon', api_id, api_hash)

async def send_with_retry(client, entity, message, max_retries=3):
    for attempt in range(max_retries):
        try:
            await client.send_message(entity, message)
            return True
        except FloodWaitError as e:
            import asyncio
            await asyncio.sleep(e.seconds)
        except PeerFloodError:
            print('Message sending limit reached. Please wait.')
            return False
        except RPCError as e:
            print(f'Error on attempt {attempt + 1}: {e}')
            if attempt == max_retries - 1:
                return False
    return False
```

### A handler with error handling

```python
@client.on(events.NewMessage(pattern=r'(?i)help'))
async def help_handler(event):
    try:
        await event.respond('Help: this is a help message.')
    except Exception as e:
        # If replying failed, stay silent
        pass
```

---

## Important Notes

1. **Always handle errors**: especially `FloodWaitError` and `PeerFloodError`
2. **Use logging**: for better troubleshooting
3. **Limit the number of retries**: to avoid infinite loops
4. **Use a decorator for error handling**: for cleaner code
5. **Don't re-raise errors**: unless you want them handled at a higher level

---

## Next Step

To learn more about the full API, read the [Full API](full-api.md) section.
