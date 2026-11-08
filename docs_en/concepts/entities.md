---
hide:
  - navigation
---

# Entity

The library makes extensive use of the concept of an "Entity". An Entity refers to any User, Chat, or Channel object that the API may return in response to certain methods, such as `GetUsersRequest`.

---

## What is an Entity?

Many methods and requests need an Entity to work. For example, you send a message to an Entity, you get the username of an Entity, and so on.

Many things act as an Entity: usernames, phone numbers, chat links, invite links, IDs, and the types themselves. This means you can use any of them wherever an Entity is needed.

!!! note "Note"
    Remember that a phone number must be in your contacts list before you can use it.

---

## Order of Preference for Entities

Use them from **best to worst**:

### 1. Input Entities

For example, `event.input_chat`, `message.input_sender`, or caching an Entity that you use often:

```python
entity = await client.get_input_entity(...)
```

### 2. Entities

If you already have the Entity, you can use it:

```python
await client.send_message(user, 'Hello!')
```

### 3. IDs

The Entity is always looked up in the cache (the `*.session` file caches the entities that have been seen).

### 4. Usernames, phone numbers, and links

The cache is used here as well (unless you call `client.get_entity()`), but a network request may be sent if the username, phone number, or link has not been found yet.

---

## Getting Entities

With a Session, the library automatically remembers ID and hash pairs:

```python
# (These examples assume you are inside an "async def")
#
# Dialogs are your open conversations.
# This method returns a list of Dialog objects that have an .entity property and other information.
#
# This is important because it populates the entity cache.
dialogs = await client.get_dialogs()

# All of these work and do the same thing
username = await client.get_entity('username')
username = await client.get_entity('t.me/username')
username = await client.get_entity('https://telegram.dog/username')

# Other kinds of Entity
channel = await client.get_entity('telegram.me/joinchat/AAAAAEkk2WdoDrB4-Q8-gg')
contact = await client.get_entity('+989123456789')
friend  = await client.get_entity(friend_id)

# Get an Entity by ID (User, Chat, or Channel)
entity = await client.get_entity(some_id)

# You can be more explicit about the type by wrapping it in a Peer
from wyngthon.tl.types import PeerUser, PeerChat, PeerChannel

my_user    = await client.get_entity(PeerUser(some_id))
my_chat    = await client.get_entity(PeerChat(some_id))
my_channel = await client.get_entity(PeerChannel(some_id))
```

!!! note "Note"
    **You do not need to fetch the Entity before using it!** Let the library do its job. Use a phone number from your contacts, a username, an ID, or an input entity (preferred but not required), whichever you have.

---

## Entity vs Input Entity

### Peer and InputPeer

On top of the regular types, the API also uses `Input*` versions. The input version of an Entity (such as `InputPeerUser`, `InputChat`, etc.) only has the minimum information that Wyng needs to identify whom you are referring to: the **ID** and **hash** of a `Peer`.

The Entity ID is the same for all users and bot accounts, but the hash **is different for each account**, so do not try to use an access hash from one account in another account, because it **will not work**.

### Peers

Sometimes, Wyng only needs to know the type of the Entity along with its ID. For this purpose, there are also `Peer` versions of Entities that only have an ID. You cannot get the hash from them because you should not need it. The library has probably already cached it.

Peers are enough to identify an Entity, but they are not enough to make requests with. You need to know their hash before you can "use them", and to know the hash you must have "met" the Entity, whether in conversations, participants, forwarded messages, and so on.

!!! note "Note"
    **You can use Peers with the library.** Behind the scenes, they are replaced with the input version. Peers are "not enough on their own", but the library does extra work to use the appropriate type.

---

## Input Entity vs Full Entity

As mentioned, API calls do not need to know all of an Entity's information, only its ID and hash. For this reason, the `client.get_input_entity()` method exists. It always uses the cache and, in most cases, does not send any API request.

When a request is sent, if you provide the full Entity (for example, a `User`), the library automatically converts it to the required `InputPeer`.

**Always** prefer `client.get_input_entity()` **over** `client.get_entity()`! Calling the latter always sends an API request to get the latest Entity information, but making requests only needs an `InputPeer`, not the full information. Only use `client.get_entity()` if you need actual information such as the username, name, title, and so on.

---

## Full Entity

In addition to `PeerUser`, `InputPeerUser`, and `User` (and their variants for chats and channels), there is also the concept of `UserFull`.

This full version has additional information, such as whether the user is blocked, notification settings, the user's bio or about text, and so on.

There is also `messages.ChatFull`, the equivalent of the full Entity for chats and channels, which also has the about section for channels.

You can get both by calling `GetFullUser`, `GetFullChat`, and `GetFullChannel`.

---

## Accessing Entities

When the documentation says "Bases: ChatGetter", it means the class you are looking at can *also* act as the class it is based on. In this case, `ChatGetter` knows how to get the *chat* that something belongs to.

```python
# Message is a ChatGetter
message.is_private
message.chat_id
await message.get_chat()
# ...and so on

# SenderGetter is similar
message.user_id
await message.get_input_sender()
message.user
# ...and so on
```

---

## Summary

TL;DR: if you are here because of "Could not find the input entity for", you should ask yourself, "How did I find this Entity through the official apps?" Now do the same thing with the library:

```python
# (These examples assume you are inside an "async def")
async with client:
    # Does it have a username? Use it!
    entity = await client.get_entity(username)
    
    # Do you have an open conversation with them? Get the dialogs.
    await client.get_dialogs()
    
    # Are they a member of a group? Get the participants.
    await client.get_participants('username')
    
    # Is the Entity the original sender of a forwarded message? Get it.
    await client.get_messages('username', 100)
    
    # Now you can use the ID, anywhere!
    await client.send_message(123456, 'Hello!')
    
    entity = await client.get_entity(123456)
    print(entity)
```

Once the library has "seen" an Entity, you can use its **numeric** ID. You cannot use Entities that the library has not seen. The library must see them *at least once* and disconnect properly.
