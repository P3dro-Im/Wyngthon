---
hide:
  - navigation
---

# Chats and Channels

This section contains examples for working with chats and channels in Wyngthon.

---

## Joining a Public Channel

```python
from wyngthon import WyngClient
from wyngthon.tl.functions.channels import JoinChannelRequest

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Get the channel's information
        channel = await client.get_entity('channel_username')
        
        # Join the channel
        await client(JoinChannelRequest(channel))
        
        print('You joined the channel')

import asyncio
asyncio.run(main())
```

---

## Leaving a Channel

```python
from wyngthon import WyngClient
from wyngthon.tl.functions.channels import LeaveChannelRequest

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Get the channel's information
        channel = await client.get_entity('channel_username')
        
        # Leave the channel
        await client(LeaveChannelRequest(channel))
        
        print('You left the channel')

import asyncio
asyncio.run(main())
```

---

## Joining via Invite Link

```python
from wyngthon import WyngClient
from wyngthon.tl.functions.messages import ImportChatInviteRequest

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Join via invite link
        # Invite link: https://t.me/joinchat/AAAAAFFszQPyPEZ7wgxLtd
        # Hash: AAAAFAFFszQPyPEZ7wgxLtd
        updates = await client(ImportChatInviteRequest('AAAAAFFszQPyPEZ7wgxLtd'))
        
        print('You joined via the invite link')

import asyncio
asyncio.run(main())
```

---

## Adding a User to a Chat

```python
from wyngthon import WyngClient
from wyngthon.tl.functions.messages import AddChatUserRequest

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Get the chat and user information
        chat = await client.get_entity('chat_username')
        user = await client.get_entity('user_username')
        
        # Add the user to the chat
        await client(AddChatUserRequest(
            chat_id=chat,
            user_id=user,
            fwd_limit=10  # Allow seeing the last 10 messages
        ))
        
        print('User added to the chat')

import asyncio
asyncio.run(main())
```

---

## Adding a User to a Channel

```python
from wyngthon import WyngClient
from wyngthon.tl.functions.channels import InviteToChannelRequest

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Get the channel and user information
        channel = await client.get_entity('channel_username')
        user = await client.get_entity('user_username')
        
        # Add the user to the channel
        await client(InviteToChannelRequest(
            channel=channel,
            users=[user]
        ))
        
        print('User added to the channel')

import asyncio
asyncio.run(main())
```

---

## Checking an Invite Link

```python
from wyngthon import WyngClient
from wyngthon.tl.functions.messages import CheckChatInviteRequest

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Check the invite link
        result = await client(CheckChatInviteRequest('hash_from_link'))
        
        print(f'Chat name: {result.chat.title}')
        print(f'Participants count: {result.participants_count}')

import asyncio
asyncio.run(main())
```

---

## Increasing a Channel's View Count

```python
from wyngthon import WyngClient
from wyngthon.tl.functions.messages import GetMessagesViewsRequest

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Get the channel's information
        channel = await client.get_entity('channel_username')
        
        # Get the recent messages
        messages = await client.get_messages(channel, limit=10)
        msg_ids = [msg.id for msg in messages]
        
        # Increment the view count
        await client(GetMessagesViewsRequest(
            peer=channel,
            id=msg_ids,
            increment=True
        ))
        
        print('View count increased')

import asyncio
asyncio.run(main())
```

!!! note "Note"
    Keep in mind that this can only be done **once or twice a day** per account.

---

## Getting the Member List

```python
from wyngthon import WyngClient
from wyngthon.tl.functions.channels import GetParticipantsRequest
from wyngthon.tl.types import ChannelParticipantsSearch

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Get the member list
        result = await client(GetParticipantsRequest(
            channel='channel_username',
            filter=ChannelParticipantsSearch(''),
            limit=100,
            offset=0
        ))
        
        for user in result.users:
            print(f'{user.first_name} {user.last_name}: {user.username}')

import asyncio
asyncio.run(main())
```

---

## Important Notes

!!! warning "Warning"
    - Only use user-adding features with friends or bot accounts
    - Do not try to add users in bulk, as your account may be flagged as a spammer
    - Always use error handling

---

## Next Steps

To learn more about working with messages, read the [Working with Messages](working-with-messages.md) section.
