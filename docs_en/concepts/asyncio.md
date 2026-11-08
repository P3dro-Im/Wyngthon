---
hide:
  - navigation
---

# Mastering asyncio

Wyngthon is built on top of asyncio. To use the library effectively, you need to understand the basic concepts of asyncio.

---

## What Is asyncio?

asyncio is a Python standard library module that lets you write asynchronous code. It allows you to perform time-consuming operations (such as network requests) without blocking the main execution of your program.

---

## Basic Concepts

### coroutine

An `async def` function is a coroutine:

```python
async def my_function():
    print('Start')
    await some_async_operation()
    print('End')
```

### await

The `await` keyword waits for an asynchronous operation to finish:

```python
async def main():
    result = await client.get_me()
    print(result.stringify())
```

### event loop

The event loop is responsible for running coroutines:

```python
import asyncio

async def main():
    # Your code runs here
    pass

# Run the event loop
asyncio.run(main())
```

---

## Using asyncio in Wyngthon

### Basic Structure

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

### Using a with Block

```python
import asyncio
from wyngthon import WyngClient

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        me = await client.get_me()
        print(me.stringify())
        
        await client.run_until_disconnected()

asyncio.run(main())
```

### Using client.loop

```python
from wyngthon import WyngClient

client = WyngClient('anon', api_id, api_hash)

async def main():
    me = await client.get_me()
    print(me.stringify())
    
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
```

---

## Practical Examples

### Sending Multiple Messages

```python
import asyncio
from wyngthon import WyngClient

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        # Send several messages
        for i in range(5):
            await client.send_message('me', f'Message {i+1}')
            await asyncio.sleep(1)  # 1 second delay

asyncio.run(main())
```

### Receiving and Processing Messages

```python
import asyncio
from wyngthon import WyngClient

async def main():
    with WyngClient('anon', api_id, api_hash) as client:
        async for message in client.iter_messages('me'):
            print(f'Message {message.id}: {message.text}')
            
            # Process messages concurrently
            await asyncio.sleep(0.1)

asyncio.run(main())
```

### Concurrent Event Handlers

```python
import asyncio
from wyngthon import WyngClient, events

client = WyngClient('anon', api_id, api_hash)

@client.on(events.NewMessage(pattern=r'(?i)hi|hello'))
async def handler1(event):
    await event.reply('Hello! (from handler 1)')

@client.on(events.NewMessage(pattern=r'(?i)help'))
async def handler2(event):
    await event.reply('Help! (from handler 2)')

async def main():
    await client.start()
    await client.run_until_disconnected()

asyncio.run(main())
```

---

## Important Notes

### 1. Use await

All methods that work with the network must be called with `await`:

```python
# Correct
me = await client.get_me()
await client.send_message('me', 'Hello')

# Wrong
me = client.get_me()  # Error!
client.send_message('me', 'Hello')  # Error!
```

### 2. Handlers must be async

Event handlers must be `async def`:

```python
# Correct
@client.on(events.NewMessage)
async def handler(event):
    await event.reply('Reply')

# Wrong
@client.on(events.NewMessage)
def handler(event):
    event.reply('Reply')  # Error!
```

### 3. Use asyncio.sleep

To add a delay in asynchronous code, use `asyncio.sleep`:

```python
import asyncio

# Correct
await asyncio.sleep(1)

# Wrong
import time
time.sleep(1)  # Blocks the event loop!
```

### 4. Use gather for concurrent operations

```python
import asyncio

async def main():
    # Run several coroutines concurrently
    await asyncio.gather(
        client.send_message('user1', 'Hello 1'),
        client.send_message('user2', 'Hello 2'),
        client.send_message('user3', 'Hello 3')
    )
```

---

## Troubleshooting asyncio Problems

### The "This event loop is already running" Error

```python
# Wrong
loop = asyncio.get_event_loop()
loop.run_until_complete(main())

# Correct
asyncio.run(main())
```

### The "Cannot run the event loop while another loop is running" Error

```python
# Wrong
async def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(some_coroutine())

# Correct
async def main():
    await some_coroutine()
```

### A Blocked Event Loop

```python
# Wrong
import time
async def main():
    time.sleep(1)  # Blocks the event loop!

# Correct
import asyncio
async def main():
    await asyncio.sleep(1)  # Does not block the event loop
```

---

## Learning Resources

- [Official asyncio documentation](https://docs.python.org/3/library/asyncio.html)
- [Async IO in Python tutorial](https://realpython.com/async-io-python/)
- [asyncio examples](https://docs.python.org/3/library/asyncio-task.html)

---

## Conclusion

asyncio is a powerful tool for writing asynchronous code in Python. By understanding the basic concepts such as coroutine, await, and the event loop, you can use Wyngthon effectively.

---

## Next Step

To learn more, read the [Examples](../examples/index.md) section.
