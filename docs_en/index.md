---
hide:
  - navigation
---

# Wyngthon Documentation

**Wyngthon** is an asyncio-based Python library designed for interacting with the Wyng API. It lets you use your own account to write a wide range of bots and scripts for Wyng.

---

## Why Wyngthon?

- **Simplicity**: A simple, readable API for interacting with Wyng
- **Performance**: asyncio support for concurrent operations
- **Rich features**: Send messages, files and photos, and manage conversations
- **Event support**: A powerful event system for automatic replies
- **Security**: Secure storage of sessions and credentials

---

## Main Documentation Sections

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } __Quick Start__

    ---

    A quick guide to get started with Wyngthon in under 5 minutes.

    [:octicons-arrow-right-24: Get started](quick-start.md)

-   :material-cog:{ .lg .middle } __Installation and Setup__

    ---

    A guide to installing the library and its optional dependencies.

    [:octicons-arrow-right-24: Install](installation.md)

-   :material-book-open-variant:{ .lg .middle } __Core Concepts__

    ---

    A comprehensive explanation of fundamental concepts such as Entity, Session and events.

    [:octicons-arrow-right-24: Learn](concepts/index.md)

-   :material-code-braces:{ .lg .middle } __Examples__

    ---

    Practical, hands-on examples for better learning.

    [:octicons-arrow-right-24: See examples](examples/index.md)

-   :material-api:{ .lg .middle } __API Reference__

    ---

    Complete API documentation for the library.

    [:octicons-arrow-right-24: Explore](api-reference.md)

-   :material-frequently-asked-questions:{ .lg .middle } __FAQ__

    ---

    Answers to common user questions.

    [:octicons-arrow-right-24: Read](faq.md)

</div>

---

## Library Overview

```python
from wyngthon import WyngClient, events

# Create the client
client = WyngClient('session_name')

# Send a message
await client.send_message('username', 'Hello!')

# Listen for events
@client.on(events.NewMessage(pattern='(?i)hello'))
async def handler(event):
    await event.reply('Hello! Welcome.')
```

---

## Prerequisites

- Python 3.8 or higher
- pip (latest version)
- Basic familiarity with asyncio in Python

---

## Useful Links

- [GitHub](https://github.com/P3dro-Im/Wyngthon)
- [Wyng](https://web.wyng.ir)
- [Full API reference](https://tl.splusthon.dev/)
