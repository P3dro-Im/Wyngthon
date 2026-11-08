---
hide:
  - navigation
---

# Full API

Wyngthon supports the full Wyng API. You can use the advanced methods for finer-grained control.

---

## Using the Raw API

### Sending a Raw Request

```python
from wyngthon.tl.functions.messages import SendMessageRequest

await client(SendMessageRequest(
    peer='username',
    message='Hello!',
    random_id=client._get_request_msg_id()
))
```

### Getting User Information

```python
from wyngthon.tl.functions.users import GetUsersRequest

users = await client(GetUsersRequest(
    id=['username1', 'username2']
))
```

### Getting Channel Information

```python
from wyngthon.tl.functions.channels import GetFullChannelRequest

full_channel = await client(GetFullChannelRequest('channel_username'))
```

---

## Advanced Methods

### Sending a File with Full Control

```python
from wyngthon.tl.functions.messages import SendMediaRequest
from wyngthon.tl.types import InputMediaUploadedDocument

# Upload the file
file = await client.upload_file('/path/to/file.jpg')

# Send the file
await client(SendMediaRequest(
    peer='username',
    media=InputMediaUploadedDocument(
        file=file,
        caption='File description'
    ),
    random_id=client._get_request_msg_id()
))
```

### Editing a Message

```python
from wyngthon.tl.functions.messages import EditMessageRequest

await client(EditMessageRequest(
    peer='username',
    id=message_id,
    message='New text'
))
```

### Deleting Messages

```python
from wyngthon.tl.functions.messages import DeleteMessagesRequest

await client(DeleteMessagesRequest(
    id=[message_id_1, message_id_2],
    revoke=True
))
```

---

## Working with Chats and Channels

### Joining a Channel

```python
from wyngthon.tl.functions.channels import JoinChannelRequest

await client(JoinChannelRequest(channel))
```

### Leaving a Channel

```python
from wyngthon.tl.functions.channels import LeaveChannelRequest

await client(LeaveChannelRequest(input_channel))
```

### Joining via Invite Link

```python
from wyngthon.tl.functions.messages import ImportChatInviteRequest

updates = await client(ImportChatInviteRequest('AAAAAEHbEkejzxUjAUCfYg'))
```

### Adding a User to a Chat

```python
from wyngthon.tl.functions.messages import AddChatUserRequest

await client(AddChatUserRequest(
    chat_id,
    user_to_add,
    fwd_limit=10  # Allow the user to see the last 10 messages
))
```

### Adding a User to a Channel

```python
from wyngthon.tl.functions.channels import InviteToChannelRequest

await client(InviteToChannelRequest(
    channel,
    [users_to_add]
))
```

---

## Working with Profiles

### Getting Full User Information

```python
from wyngthon.tl.functions.users import GetFullUserRequest

full = await client(GetFullUserRequest(user))
bio = full.full_user.about
```

### Updating Name and Bio

```python
from wyngthon.tl.functions.account import UpdateProfileRequest

await client(UpdateProfileRequest(
    first_name='New first name',
    last_name='New last name',
    about='New bio'
))
```

### Updating the Username

```python
from wyngthon.tl.functions.account import UpdateUsernameRequest

await client(UpdateUsernameRequest('new_username'))
```

### Updating the Profile Photo

```python
from wyngthon.tl.functions.photos import UploadProfilePhotoRequest

await client(UploadProfilePhotoRequest(
    await client.upload_file('/path/to/photo.jpg')
))
```

---

## Working with Media

### Downloading a Profile Photo

```python
# Download your own profile photo
await client.download_profile_photo('me')

# Download another user's profile photo
await client.download_profile_photo('username')
```

### Downloading a File from a Message

```python
async for message in client.iter_messages('username'):
    if message.photo:
        path = await message.download_media()
        print(f'File saved: {path}')
    if message.document:
        path = await message.download_media()
        print(f'File saved: {path}')
```

### Uploading a File

```python
file = await client.upload_file('/path/to/file.jpg')
```

---

## Advanced Examples

### Searching Messages

```python
from wyngthon.tl.functions.messages import SearchRequest

messages = await client(SearchRequest(
    peer='username',
    q='search term',
    limit=100
))
```

### Getting Group Participants

```python
from wyngthon.tl.functions.channels import GetParticipantsRequest
from wyngthon.tl.types import ChannelParticipantsSearch

participants = await client(GetParticipantsRequest(
    channel='username',
    filter=ChannelParticipantsSearch(''),
    limit=100,
    offset=0
))
```

### Increasing Channel View Counts

```python
from wyngthon.tl.functions.messages import GetMessagesViewsRequest

await client(GetMessagesViewsRequest(
    peer=channel,
    id=msg_ids,
    increment=True
))
```

!!! note "Note"
    Keep in mind that this can only be done **once or twice a day** per account.

---

## Important Notes

1. **Use advanced methods with caution**: some methods may lead to your account being restricted
2. **Prefer the simple methods**: unless you need fine-grained control
3. **Use error handling**: the raw API can produce more errors
4. **Read the API documentation**: https://tl.splusthon.dev/

---

## Next Step

To learn more about the comparison between Bot API and MTProto, read the [Bot API vs MTProto](botapi-vs-mtproto.md) section.
