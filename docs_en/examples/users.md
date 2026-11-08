---
hide:
  - navigation
---

# Users

This section contains examples for working with users in Wyngthon.

---

## Getting Full User Information

```python
from wyngthon import WyngClient
from wyngthon.tl.functions.users import GetFullUserRequest

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Get the user's full information
        full = await client(GetFullUserRequest('username'))
        
        # Get the bio
        bio = full.full_user.about
        print(f'Bio: {bio}')
        
        # Get other information
        user = full.users[0]
        print(f'Name: {user.first_name}')
        print(f'Username: {user.username}')

import asyncio
asyncio.run(main())
```

---

## Updating Name and Bio

```python
from wyngthon import WyngClient
from wyngthon.tl.functions.account import UpdateProfileRequest

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Update name and bio
        await client(UpdateProfileRequest(
            first_name='New first name',
            last_name='New last name',
            about='My new bio'
        ))
        
        print('Profile updated')

import asyncio
asyncio.run(main())
```

---

## Updating the Username

```python
from wyngthon import WyngClient
from wyngthon.tl.functions.account import UpdateUsernameRequest

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Update the username
        await client(UpdateUsernameRequest('new_username'))
        
        print('Username updated')

import asyncio
asyncio.run(main())
```

---

## Updating the Profile Photo

```python
from wyngthon import WyngClient
from wyngthon.tl.functions.photos import UploadProfilePhotoRequest

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Upload the new photo
        file = await client.upload_file('/path/to/photo.jpg')
        
        # Update the profile photo
        await client(UploadProfilePhotoRequest(file))
        
        print('Profile photo updated')

import asyncio
asyncio.run(main())
```

---

## Downloading a Profile Photo

```python
from wyngthon import WyngClient

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Download your own profile photo
        await client.download_profile_photo('me')
        
        # Download another user's profile photo
        await client.download_profile_photo('username')
        
        print('Profile photo downloaded')

import asyncio
asyncio.run(main())
```

---

## Getting the Contact List

```python
from wyngthon import WyngClient

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Get contacts
        contacts = await client.get_contacts()
        
        for contact in contacts:
            print(f'{contact.first_name} {contact.last_name}: {contact.username}')

import asyncio
asyncio.run(main())
```

---

## Searching for Users

```python
from wyngthon import WyngClient

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Look up a user by username
        user = await client.get_entity('username')
        print(f'User name: {user.first_name}')
        
        # Look up a user by phone number
        user = await client.get_entity('+989123456789')
        print(f'User name: {user.first_name}')

import asyncio
asyncio.run(main())
```

---

## Checking User Status

```python
from wyngthon import WyngClient

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Get the user's information
        user = await client.get_entity('username')
        
        # Check the various statuses
        print(f'Is online: {user.status}')
        print(f'Is restricted: {user.restricted}')
        print(f'Is deleted: {user.deleted}')

import asyncio
asyncio.run(main())
```

---

## Important Notes

!!! note "Note"
    - Use `GetFullUserRequest` to get a user's full information
    - Use `UpdateProfileRequest` to update the profile
    - Use `download_profile_photo` to download a profile photo
    - Always use error handling

---

## Next Steps

To learn more about working with chats and channels, read the [Chats and Channels](chats-and-channels.md) section.
