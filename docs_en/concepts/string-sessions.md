---
hide:
  - navigation
---

# String Sessions

String Sessions are a convenient way to embed login credentials directly in your code. This lets you use your account without having to store a session file on disk.

---

## Benefits of String Sessions

- **Highly portable**: It's just a text string that you can store anywhere
- **Great for cloud environments**: Such as Heroku, which has an ephemeral filesystem
- **Better security**: No need to store a sensitive file on disk
- **Easy to use**: Just put the string in your code

---

## Generating a String Session

### The simple way

```python
from wyngthon.sync import WyngClient
from wyngthon.sessions import StringSession

with WyngClient(StringSession(), api_id, api_hash) as client:
    print(client.session.save())
```

This code generates and prints a new String Session.

### Using an SQLite Session

```python
from wyngthon.sync import WyngClient
from wyngthon.sessions import StringSession

# First, log in with an SQLite Session
client = WyngClient('sqlite-session', api_id, api_hash)

# Then convert it to a String Session
string = StringSession.save(client.session)
print(string)
```

### Using a regular WyngClient

```python
from wyngthon import WyngClient
from wyngthon.sessions import StringSession

client = WyngClient(StringSession())
await client.start()

# Get the String Session
string_session = client.session.save()
print(string_session)
```

---

## Using a String Session

### Loading and using it

```python
string = '1aaNk8EX-YRfwoRsebUkugFvht6DUPi_Q25UOCzOAqzc...'

with WyngClient(StringSession(string), api_id, api_hash) as client:
    client.loop.run_until_complete(client.send_message('me', 'Hello'))
```

### Loading from a text file

```python
# Save the String Session to a text file
with open('session.txt', 'w') as f:
    f.write(string_session)

# Load it from the text file
with open('session.txt', 'r') as f:
    string = f.read()

with WyngClient(StringSession(string), api_id, api_hash) as client:
    # Use the client
    pass
```

### Loading from an environment variable

```python
import os
from wyngthon import WyngClient
from wyngthon.sessions import StringSession

string = os.environ.get('SESSION_STRING')
with WyngClient(StringSession(string), api_id, api_hash) as client:
    # Use the client
    pass
```

---

## Complete Example

### Creating and saving a String Session

```python
from wyngthon import WyngClient
from wyngthon.sessions import StringSession

async def create_session():
    client = WyngClient(StringSession())
    await client.start()
    
    # Save the String Session
    string = client.session.save()
    
    # Save it to a file
    with open('my_session.txt', 'w') as f:
        f.write(string)
    
    print('String Session saved:')
    print(string)
    
    await client.disconnect()

import asyncio
asyncio.run(create_session())
```

### Using a saved String Session

```python
from wyngthon import WyngClient
from wyngthon.sessions import StringSession

async def use_session():
    # Load the String Session from a file
    with open('my_session.txt', 'r') as f:
        string = f.read()
    
    # Create the client
    with WyngClient(StringSession(string), api_id, api_hash) as client:
        # Get user information
        me = await client.get_me()
        print(f'Logged in as: {me.first_name}')
        
        # Send a message
        await client.send_message('me', 'Hello from String Session!')

import asyncio
asyncio.run(use_session())
```

---

## Security Tips

!!! warning "Warning"
    **Keep your String Session safe!** Anyone with this string can use it to log in to your account and do whatever they want.
>
> This is similar to leaking `*.session` files online, but leaking a string is easier than leaking a file.

### Important security tips

1. **Never put a String Session in online source code**
2. **Use environment variables to store the String Session**
3. **Git-ignore text files that contain a String Session**
4. **Use encryption to store the String Session**
5. **Restrict access to files that contain a String Session**

---

## Comparison with Other Methods

| Method | Pros | Cons |
|------|--------|--------|
| **SQLite Session** | Default, persistent | Requires a file on disk |
| **String Session** | Highly portable | Requires managing a string |
| **Memory Session** | Fast | Data is kept in memory (temporary) |

---

## Troubleshooting

### Invalid String Session error

If you get an error such as "Invalid session":

1. Make sure you copied the String Session correctly
2. Make sure you are using the same original API ID and hash
3. Generate the String Session again

### String Session doesn't work

If the String Session doesn't work:

1. Make sure the String Session hasn't expired
2. Make sure your account hasn't been banned
3. Try again with a new String Session

---

## Next Step

To learn more about error handling, read the [Error Handling](errors.md) section.
