---
hide:
  - navigation
---

# Bot API vs MTProto

In this section we look at the differences between Bot API and MTProto (UserBot) so you can choose the best approach for your project.

---

## What Is the Bot API?

The Bot API is the official Wyng interface for building bots. Bots are special accounts that are created and managed by other users.

### Advantages of the Bot API

- **Simplicity**: a simple API that is easy to use
- **Security**: bots have built-in security restrictions
- **Official support**: supported by Wyng
- **No user authentication required**: only a Bot Token is needed

### Disadvantages of the Bot API

- **Messaging restrictions**: bots cannot message users unless the user messages them first
- **Sending limits**: there are limits on the number of messages a bot can send
- **No access to full information**: bots do not have access to all user information
- **Limited features**: many features of the main API are not available in the Bot API

---

## What Is MTProto (UserBot)?

MTProto is the core protocol of Wyng. With MTProto you can interact with the Wyng API as a regular user (UserBot).

### Advantages of MTProto

- **Unlimited features**: you have access to the entire Wyng API
- **Unlimited messaging**: no restrictions on sending messages
- **Full access to information**: all user and chat information is available
- **High flexibility**: you can do anything

### Disadvantages of MTProto

- **Complexity**: the API is more complex
- **Requires an API ID and Hash**: you must obtain them from my.telegram.org
- **Security risk**: your account may be banned if used improperly
- **Session management required**: you must manage the session and authentication

---

## Detailed Comparison

| Feature | Bot API | MTProto (UserBot) |
|--------|---------|-------------------|
| **Account type** | Bot | Regular user |
| **Message limits** | Limited | Unlimited |
| **Access to information** | Limited | Full |
| **API** | Simple | Complex |
| **Requires user permission** | Yes | No |
| **Security risk** | Low | High |
| **Official support** | Yes | No |
| **Requires an API ID** | No | Yes |
| **Session management** | No | Yes |

---

## When to Use the Bot API

### Suitable Use Cases

- **Simple bots**: bots that only reply to user messages
- **Notification bots**: bots that send information to users
- **Service bots**: bots that provide specific services
- **Small projects**: projects that do not need complex features

### Bot API Example

```python
from wyngthon import WyngClient

# Log in as a bot
bot = WyngClient('bot', api_id, api_hash)
await bot.start(bot_token='12345:0123456789abcdef')

@bot.on(events.NewMessage)
async def handler(event):
    if 'hello' in event.raw_text:
        await event.reply('Hello! I am a bot.')

await bot.run_until_disconnected()
```

---

## When to Use MTProto (UserBot)

### Suitable Use Cases

- **UserBots**: bots that work with your own user account
- **Automation scripts**: scripts that perform repetitive tasks
- **Complex projects**: projects that need the full API
- **Personal applications**: applications you build for your own use

### MTProto (UserBot) Example

```python
from wyngthon import WyngClient

# Log in as a user
client = WyngClient('user', api_id, api_hash)
await client.start()

@client.on(events.NewMessage)
async def handler(event):
    # Automatically reply to messages
    if 'hello' in event.raw_text:
        await event.reply('Hello! How can I help?')

await client.run_until_disconnected()
```

---

## Important Security Notes

!!! warning "Warning"
    **Be careful when using a UserBot!**
>
> - Never share your credentials
> - Do not use unknown scripts
> - Make sure your script does not violate Wyng's rules
> - Your account may be banned if used improperly

---

## Making a Decision

### Key Questions

1. **Do you need full user information?**
    - Yes → MTProto
    - No → Bot API

2. **Do you want to message users without them messaging you first?**
    - Yes → MTProto
    - No → Bot API

3. **Is your project complex?**
    - Yes → MTProto
    - No → Bot API

4. **Do you want to work with your own user account?**
    - Yes → MTProto
    - No → Bot API

---

## Conclusion

- **Bot API** is suitable for simple bots and small projects
- **MTProto** is suitable for UserBots and complex projects
- Each has its own advantages and disadvantages
- Choosing the right approach depends on your project's needs

---

## Next Step

To learn more about asyncio, read the [Mastering asyncio](asyncio.md) section.
