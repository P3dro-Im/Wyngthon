---
hide:
  - navigation
---

# API Reference

This section contains the complete API documentation for the Wyngthon library.

---

## The WyngClient Class

The main class of the library for interacting with Wyng.

### Constructor

```python
WyngClient(session=None, api_id=None, api_hash=None, 
              connection_retries=None, timeout=timedelta(seconds=60), 
              request_retries=None, connection=None, 
              proxy=None, local_addr=None)
```

### Parameters

| Parameter | Type | Default | Description |
|---------|-----|---------|---------|
| session | str/Session | None | Session name or a Session object |
| api_id | int | None | API ID from my.telegram.org |
| api_hash | str | None | API hash from my.telegram.org |
| connection_retries | int | None | Number of connection retry attempts |
| timeout | timedelta | 60 seconds | Timeout for requests |
| request_retries | int | None | Number of request retry attempts |
| connection | class | None | Connection type |
| proxy | dict | None | Proxy settings |
| local_addr | tuple | None | Local address |

---

## Message Sending Methods

### send_message

```python
async def send_message(entity, message=None, *, parse_mode=None, 
                       link_preview=None, file=None, force_document=None, 
                       clear_draft=None, background=None, 
                       supports_streaming=None, schedule=None, 
                       noforwards=None, comment_to=None, 
                       reply_to=None, top_msg_id=None)
```

**Parameters:**

- `entity`: the message destination (username, phone number, chat ID)
- `message`: the message text
- `parse_mode`: the parse mode (markdown/html)
- `link_preview`: whether to show a link preview
- `file`: a file to send
- `reply_to`: reply to a specific message

**Example:**

```python
await client.send_message('username', 'Hello!')
await client.send_message('me', 'Message with **bold**')
await client.send_message('me', 'https://example.com', link_preview=False)
```

---

### send_file

```python
async def send_file(entity, file, *, caption=None, 
                    force_document=None, thumb=None, 
                    voice_note=None, video_note=None, 
                    attributes=None, supports_streaming=None, 
                    schedule=None, noforwards=None, 
                    reply_to=None, top_msg_id=None, 
                    comment_to=None, parse_mode=(), 
                    buttons=None, silent=None, 
                    background=None, clear_draft=None, 
                    video_start_ts=None, duration=None, 
                    title=None, performer=None, 
                    force_file=None, file_size=None, 
                    chunk_size=None, file_names=None, 
                    workers=1, api_hash=None)
```

**Parameters:**

- `entity`: the file destination
- `file`: the file path or a file object
- `caption`: the file caption

**Example:**

```python
await client.send_file('me', '/path/to/photo.jpg')
await client.send_file('me', '/path/to/file.pdf', caption='Important file')
```

---

## Message Retrieval Methods

### get_messages

```python
async def get_messages(entity, limit=None, *, offset_date=None, 
                       offset_id=None, add_offset=None, 
                       search=None, from_user=None, 
                       ids=None, reverse=None, 
                       wait_time=None)
```

**Parameters:**

- `entity`: the source of the messages
- `limit`: the number of messages
- `search`: the search term
- `ids`: the message IDs

**Example:**

```python
messages = await client.get_messages('me', limit=10)
messages = await client.get_messages('me', search='search term')
message = await client.get_messages('me', ids=123)
```

---

### iter_messages

```python
def iter_messages(entity, limit=None, *, offset_date=None, 
                  offset_id=None, add_offset=None, 
                  search=None, from_user=None, 
                  ids=None, reverse=None, 
                  wait_time=None)
```

**Example:**

```python
async for message in client.iter_messages('me', limit=10):
    print(f'{message.id}: {message.text}')
```

---

## Message Editing Methods

### edit_message

```python
async def edit_message(entity=None, message=None, *, 
                       text=None, parse_mode=None, 
                       link_preview=None, file=None, 
                       video_start_ts=None, 
                       force_document=None, 
                       schedule=None, noforwards=None)
```

**Example:**

```python
await client.edit_message('username', message_id, 'New text')
```

---

### delete_messages

```python
async def delete_messages(entity, messages, *, revoke=None)
```

**Example:**

```python
await client.delete_messages('username', [123, 456])
```

---

## Entity Methods

### get_entity

```python
async def get_entity(entity)
```

**Example:**

```python
user = await client.get_entity('username')
user = await client.get_entity('+989123456789')
user = await client.get_entity(123456)
```

---

### get_input_entity

```python
async def get_input_entity(entity)
```

**Example:**

```python
input_user = await client.get_input_entity('username')
```

---

## Media Methods

### download_profile_photo

```python
async def download_profile_photo(entity, file=None, *, 
                                  big=None, download_big=None)
```

**Example:**

```python
await client.download_profile_photo('me')
await client.download_profile_photo('username')
```

---

### upload_file

```python
async def upload_file(file, *, file_size=None, 
                      part_size_kb=None, 
                      file_name=None, 
                      use_cache=None)
```

**Example:**

```python
file = await client.upload_file('/path/to/file.jpg')
```

---

## Events

### NewMessage

```python
@client.on(events.NewMessage)
async def handler(event):
    print(event.raw_text)
```

### NewMessage Parameters

| Parameter | Type | Description |
|---------|-----|---------|
| incoming | bool | Incoming messages |
| outgoing | bool | Outgoing messages |
| pattern | str | A regex to filter by |
| chats | list | Specific chats |
| blacklist_chats | bool | Blacklist the chats |

---

### MessageEdited

```python
@client.on(events.MessageEdited)
async def handler(event):
    print('Message edited:', event.raw_text)
```

---

### MessageDeleted

```python
@client.on(events.MessageDeleted)
async def handler(event):
    print('Message deleted:', event.message_id)
```

---

### CallbackQuery

```python
@client.on(events.CallbackQuery)
async def handler(event):
    print('Button clicked:', event.data)
    await event.answer('Answer')
```

---

### ChatAction

```python
@client.on(events.ChatAction)
async def handler(event):
    if event.user_joined:
        print('A new member joined')
    if event.user_left:
        print('A member left')
```

---

## Errors

### RPCError

The base error of the Wyng API.

### FloodWaitError

The mandatory wait error.

```python
from wyngthon.errors import FloodWaitError

try:
    await client.send_message('username', 'Hello!')
except FloodWaitError as e:
    print(f'Wait {e.seconds} seconds')
```

---

### PeerFloodError

The message sending limit error.

```python
from wyngthon.errors import PeerFloodError

try:
    await client.send_message('username', 'Hello!')
except PeerFloodError:
    print('Message sending limit reached')
```

---

## Session

### StringSession

```python
from wyngthon.sessions import StringSession

# Create a StringSession
session = StringSession()

# Use a StringSession
client = WyngClient(StringSession(string), api_id, api_hash)

# Save the StringSession
string = client.session.save()
```

---

## Resources

- [Complete API Reference](https://tl.splusthon.dev/)
- [Wyngthon on GitHub](https://github.com/P3dro-Im/Wyngthon)
