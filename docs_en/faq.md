---
hide:
  - navigation
---

# Frequently Asked Questions

Answers to common Wyngthon user questions.

---

## Installation and Setup Questions

### How do I install Wyngthon?

```bash
pip install wyngthon
```

### How do I install the development version?

```bash
pip install --upgrade https://github.com/P3dro-Im/Wyngthon/archive/refs/heads/main.zip
```

### How do I verify the installation?

```bash
python3 -c "import wyngthon; print(wyngthon.__version__)"
```

### What are the optional dependencies?

- **cryptg**: Faster encryption
- **Pillow**: Automatic image resizing
- **aiohttp**: Downloading WebDocument files
- **hachoir**: Extracting metadata from files

---

## Authentication Questions

### How do I get an API ID and Hash?

1. Go to [my.telegram.org](https://my.telegram.org/)
2. Log in with your account's phone number
3. Click "API Development tools"
4. Fill in your application's details
5. Click "Create application"

### Can I use Wyngthon without an API ID?

Yes, Wyngthon has default API credentials:

```python
from wyngthon import WyngClient
from wyngthon.sessions import StringSession

client = WyngClient(StringSession())
client.start()
```

### How do I log in as a bot?

```python
from wyngthon.sync import WyngClient

api_id = 12345
api_hash = '0123456789abcdef0123456789abcdef'
bot_token = '12345:0123456789abcdef0123456789abcdef'

bot = WyngClient('bot', api_id, api_hash).start(bot_token=bot_token)
```

---

## Messaging Questions

### How do I send a message?

```python
await client.send_message('username', 'Hello!')
await client.send_message('me', 'Hello, myself!')
await client.send_message('+989123456789', 'Hello my friend!')
```

### How do I send a file?

```python
await client.send_file('me', '/path/to/file.jpg')
await client.send_file('me', '/path/to/file.pdf', caption='Description')
```

### How do I receive messages?

```python
messages = await client.get_messages('me', limit=10)
for message in messages:
    print(message.text)
```

### How do I reply to a message?

```python
message = await client.get_messages('me', ids=123)
await message.reply('This is a reply!')
```

---

## Event Questions

### How do I respond to new messages?

```python
from wyngthon import WyngClient, events

client = WyngClient('anon', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    if 'hello' in event.raw_text:
        await event.reply('Hello! How can I help?')

client.start()
client.run_until_disconnected()
```

### How do I respond only to certain messages?

```python
@client.on(events.NewMessage(pattern=r'(?i)hi|hello'))
async def handler(event):
    await event.reply('Hello!')

@client.on(events.NewMessage(outgoing=True))
async def handler_outgoing(event):
    print('Outgoing message:', event.raw_text)
```

---

## Session Questions

### What is a Session?

A Session is a file that stores authentication information and the entity cache.

### What is a StringSession?

StringSession is a type of Session that stores its data as a string:

```python
from wyngthon.sessions import StringSession

session = StringSession()
string = session.save()
```

### How do I save a Session?

```python
# Save as a file
client = WyngClient('session_name', api_id, api_hash)

# Save as a string
string = client.session.save()
```

---

## Troubleshooting Questions

### What is FloodWaitError?

It is an error that occurs when you send requests too quickly. You need to wait:

```python
from wyngthon.errors import FloodWaitError

try:
    await client.send_message('username', 'Hello!')
except FloodWaitError as e:
    print(f'Wait {e.seconds} seconds')
```

### What is PeerFloodError?

It is an error that occurs when you have reached the message-sending limit:

```python
from wyngthon.errors import PeerFloodError

try:
    await client.send_message('username', 'Hello!')
except PeerFloodError:
    print('Message sending limit reached. Please wait.')
```

### How do I handle errors?

```python
from wyngthon.errors import RPCError, FloodWaitError, PeerFloodError

async def safe_send(client, entity, message):
    try:
        await client.send_message(entity, message)
        return True
    except FloodWaitError as e:
        import asyncio
        await asyncio.sleep(e.seconds)
        return True
    except PeerFloodError:
        print('Message sending limit reached')
        return False
    except RPCError as e:
        print(f'Error: {e}')
        return False
```

---

## Advanced Questions

### How do I use a proxy?

```python
proxy = {
    'proxy_type': 'socks5',
    'addr': '1.1.1.1',
    'port': 5555,
    'username': 'foo',
    'password': 'bar',
    'rdns': True
}

client = WyngClient('anon', api_id, api_hash, proxy=proxy)
```

### How do I use an MTProto Proxy?

```python
from wyngthon import WyngClient, connection

client = WyngClient(
    'anon', api_id, api_hash,
    connection=connection.ConnectionTcpMTProxyRandomizedIntermediate,
    proxy=('mtproxy.example.com', 2002, 'secret')
)
```

### How do I run multiple clients at the same time?

```python
import asyncio
from wyngthon import WyngClient

async def run_client(name, api_id, api_hash):
    client = WyngClient(name, api_id, api_hash)
    await client.start()
    await client.run_until_disconnected()

async def main():
    await asyncio.gather(
        run_client('client1', api_id1, api_hash1),
        run_client('client2', api_id2, api_hash2)
    )

asyncio.run(main())
```

---

## Security Questions

### How do I keep my credentials safe?

1. Use environment variables
2. Do not expose credentials in your code
3. Do not share session files online
4. Use encryption

### Is Wyngthon safe?

Wyngthon is a third-party library. Be careful to:

- Download it from trusted sources
- Not share your credentials with anyone
- Follow Wyng's rules

---

## Development Questions

### How do I report a bug?

Go to [GitHub Issues](https://github.com/P3dro-Im/Wyngthon/issues/) and create a new issue.

### How do I contribute?

1. Fork the repository
2. Make your changes
3. Submit a Pull Request

### How do I read the documentation?

- [Full API reference](https://tl.splusthon.dev/)
- [Wyngthon GitHub](https://github.com/P3dro-Im/Wyngthon)

---

## Other Questions

### What is Wyngthon?

Wyngthon is an asyncio-based Python library designed for interacting with the Wyng API.

### Which Python versions does Wyngthon support?

Python 3.8 or higher.

### Is Wyngthon free?

Yes, Wyngthon is completely free and open source.

### How do I use Wyngthon?

Read the documentation and follow the examples.
