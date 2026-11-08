---
hide:
  - navigation
---

# Word of Warning

When using Wyngthon, it is important to be aware of Wyng's rules and limits so that your account does not get banned.

---

## Important Wyng Rules

### 1. No Spam

- **Never** send promotional or spam messages
- **Never** send messages in bulk
- **Never** message users without their permission

### 2. Respect Privacy

- **Never** collect users' personal information without permission
- **Never** share private information
- **Never** enter private chats without permission

### 3. No Rule Violations

- **Never** use Wyngthon for illegal purposes
- **Never** violate Wyng's rules
- **Never** hack other people's accounts

---

## Technical Limits

### Message Sending Limits

- **FloodWaitError**: if you send messages too quickly, you have to wait
- **PeerFloodError**: if you hit the message sending limit, you have to wait

### Request Limits

- **Requests per second**: a limit on the number of API requests
- **Requests per day**: a limit on the total number of requests

### Account Limits

- **Account ban**: if you do not follow the rules, your account may be banned
- **Account restriction**: if you do not respect the limits, your account may be restricted

---

## Security Tips

### 1. Protecting Your Credentials

```python
# Wrong - never expose credentials in your code
api_id = 12345
api_hash = '0123456789abcdef'

# Right - use environment variables
import os
api_id = int(os.environ.get('API_ID'))
api_hash = os.environ.get('API_HASH')
```

### 2. Protecting Your Session

```python
# Wrong - never share your Session online
session_string = '1aaNk8EX-YRfwoRsebUkugFvht6DUPi_Q25UOCzOAqzc...'

# Right - use encryption
import os
session_string = os.environ.get('SESSION_STRING')
```

### 3. Limiting Access

```python
# Wrong - never grant full access
client = WyngClient('session', api_id, api_hash)
await client.start()

# Right - grant only the permissions that are needed
# (this example is only a concept; Wyngthon manages permissions automatically)
```

---

## Best Practices

### 1. Use Error Handling

```python
from wyngthon.errors import FloodWaitError, PeerFloodError, RPCError

async def safe_send(client, entity, message):
    try:
        await client.send_message(entity, message)
        return True
    except FloodWaitError as e:
        import asyncio
        await asyncio.sleep(e.seconds)
        return True
    except PeerFloodError:
        print('Message sending limit reached. Please wait.')
        return False
    except RPCError as e:
        print(f'Error: {e}')
        return False
```

### 2. Use Logging

```python
import logging
from wyngthon import WyngClient, events

logging.basicConfig(
    format='[%(levelname) %(asctime)s] %(name)s: %(message)s',
    level=logging.WARNING
)

client = WyngClient('anon', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    logging.info(f'New message: {event.raw_text}')
```

### 3. Limit the Number of Requests

```python
import asyncio

async def rate_limited_send(client, entities, message, delay=1):
    for entity in entities:
        await client.send_message(entity, message)
        await asyncio.sleep(delay)  # Delay between requests
```

### 4. Use a String Session in Cloud Environments

```python
from wyngthon import WyngClient
from wyngthon.sessions import StringSession

# For cloud environments such as Heroku
import os
session_string = os.environ.get('SESSION_STRING')
client = WyngClient(StringSession(session_string), api_id, api_hash)
```

---

## Troubleshooting Common Problems

### Banned Account

If your account has been banned:

1. Contact Wyng support
2. Find out why the account was banned
3. Learn from your past mistakes

### FloodWaitError

If you received a FloodWaitError:

1. Respect the waiting time
2. Reduce the rate at which you send messages
3. Use a delay between requests

### PeerFloodError

If you received a PeerFloodError:

1. Respect the waiting time
2. Reduce the number of messages you send
3. Avoid sending messages in bulk

---

## Useful Resources

- [Wyng Terms](https://web.wyng.ir/terms)
- [Wyng API Documentation](https://core.splus.ir/)
- [Wyngthon on GitHub](https://github.com/P3dro-Im/Wyngthon)

---

## Conclusion

By following the rules and security tips, you can use Wyngthon safely and effectively. Always follow best practices and keep a close eye on your account.
