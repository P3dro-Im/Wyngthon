---
hide:
  - navigation
---

# Session

Sessions are an important part of the library that store authentication information and the entity cache.

---

## What is a Session?

The first parameter you pass to the `WyngClient` constructor is `session`, and by default it is the session name (or full path). This means that if you create `WyngClient('anon')` and connect, an `anon.session` file is created in the current directory.

!!! note "Note"
    If you pass a string, the file will be in the current working directory, although you can also pass absolute paths.

The session file has enough information to log in without sending the code again, so if you have to enter the code more than once, you may be changing the working directory, renaming or deleting the file, or using random names.

---

## Session File Contents

The database files, which use `sqlite3`, contain the information needed to communicate with Wyng servers, such as:

- The server IP address and port
- The authorization key (for encrypting messages)
- Information about the entities you have seen
- The access_hash of users and channels

### Entity cache

By default, these files store all the input entities you have seen so that you can get user or channel information using only their ID. Wyng **will not send** the `access_hash` needed to retrieve more information if it thinks you have already seen them. This is why the library needs to store this information offline.

### Disabling entity storage

If you do not intend to work with events, or you do not need to cache the `access_hash` associated with Entity IDs, you can disable this by setting `client.session.save_entities = False`.

---

## Session Storage Types

If you do not want to use the default SQLite Session storage, you can use one of the other implementations or your own.

!!! note "Note"
    Although it is often not the case, SQLite may be slow enough to be noticeable, in which case you can use a different storage. Note that this is rare and most people will not have this problem.

### Available implementations

Wyngthon has three implementations of the abstract `Session` class:

```python
from wyngthon.sessions import MemorySession, SQLiteSession, StringSession
```

1. **MemorySession**: Stores session data in memory.
2. **SQLiteSession**: Stores session data in an SQLite database on disk. The default.
3. **StringSession**: Stores session data in memory, but can be saved as a string.

### Using StringSession

```python
from wyngthon.sync import WyngClient
from wyngthon.sessions import StringSession

with WyngClient(StringSession(string), api_id, api_hash) as client:
    ...  # use the client
    
    # Save the session as a string
    string = client.session.save()

# You can also save any other type of session as a string
client = WyngClient('sqlite-session', api_id, api_hash)
string = StringSession.save(client.session)
```

---

## Creating Custom Storage

The easiest way to create your own custom storage implementation is to use `MemorySession` as the base and look at how `SQLiteSession` or one of the community implementations works.

You can find the relevant Python files in the `sessions/` directory of the Wyngthon repository.

After creating your own implementation, you can add it to the list of community-maintained session implementations.

---

## String Sessions

`StringSession` is a convenient way to embed login credentials directly in your code for very easy portability, since they only need a single string to log in without asking for a phone number and code (or to start faster if you use a bot token).

### Generating a String Session

The easiest way to generate a StringSession is as follows:

```python
from wyngthon.sync import WyngClient
from wyngthon.sessions import StringSession

with WyngClient(StringSession(), api_id, api_hash) as client:
    print(client.session.save())
```

Think of this as a way to export your authorization key (what is needed to log in to your account). It prints a string to standard output (probably your terminal).

!!! warning "Warning"
    **Keep this string safe!** Anyone with this string can use it to log in to your account and do whatever they want.
>
> This is similar to leaking `*.session` files online, but leaking a string is easier than leaking a file.

### Using a String Session

Once you have the string (which is a bit long), load it into your script somehow. You can use a regular text file and `open(...).read()`, or store it directly in a variable:

```python
string = '1aaNk8EX-YRfwoRsebUkugFvht6DUPi_Q25UOCzOAqzc...'
with WyngClient(StringSession(string), api_id, api_hash) as client:
    client.loop.run_until_complete(client.send_message('me', 'Hello'))
```

These strings are really convenient for use in places like Heroku, because their ephemeral filesystem deletes external files after the program ends.

---

## Important Notes

1. **Session safety**: Session files are sensitive and should not be shared online.
2. **Renaming the file**: If you rename or move the session file, you may have to log in again.
3. **Backups**: Always back up your session files.
4. **StringSession**: Suitable for deployment in cloud environments such as Heroku.

---

## Next Steps

To learn more about events, read the [Events](events.md) section.
