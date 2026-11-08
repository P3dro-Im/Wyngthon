---
hide:
  - navigation
---

# Core Concepts

In this section you will learn the fundamental concepts of Wyngthon. Understanding them is essential for using the library effectively.

---

## Table of Contents

<div class="grid cards" markdown>

-   :material-account-group:{ .lg .middle } __Entity__

    ---

    A comprehensive guide to Entities and how to use them.

    [:octicons-arrow-right-24: Learn more](entities.md)

-   :material-database:{ .lg .middle } __Session__

    ---

    A guide to Sessions and how to manage them.

    [:octicons-arrow-right-24: Learn more](sessions.md)

-   :material-bell-ring:{ .lg .middle } __Events__

    ---

    A powerful event system for automatic responses.

    [:octicons-arrow-right-24: Learn more](events.md)

-   :material-key:{ .lg .middle } __String Sessions__

    ---

    A guide to using String Sessions.

    [:octicons-arrow-right-24: Learn more](string-sessions.md)

-   :material-alert-circle:{ .lg .middle } __Error Handling__

    ---

    A guide to handling errors and troubleshooting.

    [:octicons-arrow-right-24: Learn more](errors.md)

-   :material-api:{ .lg .middle } __Full API__

    ---

    Using the full Wyng API.

    [:octicons-arrow-right-24: Learn more](full-api.md)

-   :material-compare:{ .lg .middle } __Bot API vs MTProto__

    ---

    A comparison of the different approaches to bot development.

    [:octicons-arrow-right-24: Learn more](botapi-vs-mtproto.md)

-   :material-language-python:{ .lg .middle } __Mastering asyncio__

    ---

    A comprehensive guide to using asyncio effectively.

    [:octicons-arrow-right-24: Learn more](asyncio.md)

</div>

---

## The Entity Concept

An **Entity** refers to any User, Chat, or Channel object that the API returns in response to certain methods, such as `GetUsersRequest`.

### What can be used as an Entity?

- **Usernames**: such as `username`
- **Phone numbers**: such as `+989123456789`
- **Chat links**: such as `t.me/username`
- **Invite links**: such as `t.me/joinchat/AAAAAFFszQPyPEZ7wgxLtd`
- **IDs**: such as `123456`
- **The objects themselves**: such as `User`, `Chat`, or `Channel`

### Order of preference for Entities

Use them from **best to worst**:

1. **Input Entities**: such as `event.input_chat` or `message.input_sender`
2. **Entities**: such as `user` or `channel` (if you already have them)
3. **IDs**: the session cache is used
4. **Usernames, phone numbers, and links**: the cache is used unless you call `client.get_entity()`

---

## The Session Concept

A **Session** is an important part of the library that stores authentication information and the entity cache.

### Session types

1. **SQLiteSession**: The default. Data is stored in an SQLite file.
2. **MemorySession**: Data is stored in memory.
3. **StringSession**: Data is stored in memory but can be saved as a string.

### The session file

When you create `WyngClient('anon')`, an `anon.session` file is created in the current directory. This file contains:

- The server IP address and port
- The authorization key
- Information about the entities you have seen
- The access_hash of users and channels

---

## The Events Concept

**Events** are used to receive notifications about new messages, members joining, typing, and more.

### Main event types

- **NewMessage**: A new message was received
- **MessageEdited**: A message was edited
- **MessageDeleted**: A message was deleted
- **CallbackQuery**: An inline button was clicked
- **ChatAction**: A new member joined or left
- **InlineQuery**: An inline query was received
- **UserUpdate**: A user's information changed

### Event usage example

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

---

## Understanding Entities in Events

When you need the user or chat in which an event occurred, you **must** use the following methods:

```python
async def handler(event):
    # Correct
    chat = await event.get_chat()
    sender = await event.get_sender()
    chat_id = event.chat_id
    sender_id = event.sender_id
    
    # Wrong - do not do this
    chat = event.chat
    sender = event.sender
    chat_id = event.chat.id
    sender_id = event.sender.id
```

Events are similar to messages, but they do not carry all of a message's information! When you fetch a message manually, it has all the necessary information. But when you receive an update about a message, it **does not have all the information**, so you must use **methods**, not properties.

---

## The Full API

Wyngthon supports the full Wyng API. You can use advanced methods for finer control.

### Raw API usage example

```python
from wyngthon.tl.functions.messages import SendMessageRequest

await client(SendMessageRequest(
    peer='username',
    message='Hello!',
    random_id=client._get_request_msg_id()
))
```

---

## Bot API vs MTProto

| Feature | Bot API | MTProto (UserBot) |
|--------|---------|-------------------|
| Account type | Bot | Regular user |
| Message limits | Limited | Unlimited |
| Access to information | Limited | Full |
| API | Simple | Complex |
| Requires user permission | Yes | No |

---

## Mastering asyncio

Wyngthon is built on asyncio. To use it effectively, you need to understand the basic concepts of asyncio.

### Basics

```python
import asyncio
from wyngthon import WyngClient

async def main():
    client = WyngClient('anon', api_id, api_hash)
    
    # Use await for asynchronous operations
    me = await client.get_me()
    print(me.stringify())
    
    # Run the event loop
    await client.run_until_disconnected()

# Run the main loop
asyncio.run(main())
```

### Key points

1. All methods that perform network operations must be called with `await`
2. Event handlers must be `async def`
3. Use `client.loop.run_until_complete()` to run asynchronous code from synchronous code

---

## Next Steps

To learn more, read the following sections:

- [Examples](../examples/index.md): Practical, real-world examples
- [API Reference](../api-reference.md): Complete API documentation
