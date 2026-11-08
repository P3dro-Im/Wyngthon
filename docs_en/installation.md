---
hide:
  - navigation
---

# Installation and Setup

A guide to installing Wyngthon and configuring your development environment.

---

## Installing Python

Wyngthon is a Python library, so you first need to download and install Python from [python.org](https://www.python.org/downloads/) (version 3.8 or higher is recommended).

!!! note "Note"
    After installing Python, upgrade pip to the latest version:

```bash
python3 -m pip install --upgrade pip
```

---

## Installing the Library

To install Wyngthon, run the following command:

```bash
python3 -m pip install --upgrade wyngthon
```

---

## Installing the Development Version

If you want the latest unreleased changes:

```bash
python3 -m pip install --upgrade https://github.com/P3dro-Im/Wyngthon/archive/refs/heads/main.zip
```

!!! warning "Warning"
    The development version may contain bugs and is not recommended for production use. However, when reporting a library bug, you should test against this version.

---

## Verifying the Installation

To make sure the library is installed correctly, run the following command:

```bash
python3 -c "import wyngthon; print(wyngthon.__version__)"
```

The library version should be displayed in the output.

---

## Optional Dependencies

### cryptg

If cryptg is installed, **the library runs much faster** because encryption and decryption are performed in C instead of Python. If your code deals with a large number of events or downloads/uploads many files, you will notice a significant speedup.

```bash
pip install cryptg
```

### Pillow

If pillow is installed, large images are automatically resized when sending photos to avoid the "invalid image" error.

```bash
pip install pillow
```

### aiohttp

If aiohttp is installed, the library will be able to download WebDocument media files.

```bash
pip install aiohttp
```

### hachoir

If hachoir is installed, metadata is extracted when sending files. Wyng uses this information to display the performer, artist, title, duration and size of videos.

```bash
pip install hachoir
```

---

## Installing Common Dependencies

If your system is apt-based, you can install the common dependencies with the following commands:

```bash
apt update
apt install clang lib{jpeg-turbo,webp}-dev python{,-dev} zlib-dev
pip install -U --user setuptools
pip install -U --user wyngthon cryptg pillow
```

---

## Installing Proxy Support

If you need to use a proxy to access Wyng, you must install the python-socks package:

```bash
pip install python-socks[asyncio]
```

Then pass the proxy to the client:

```python
WyngClient('session_name', api_id, api_hash, proxy=proxy_config)
```

---

## Troubleshooting Installation

### ImportError

If you get the error `ImportError: cannot import name 'WyngClient'`:

1. Make sure your script is not named `wyngthon.py`
2. Reinstall the library: `pip install --upgrade wyngthon`

### Dependency installation errors

If you have trouble installing dependencies:

```bash
pip install --upgrade setuptools wheel
pip install --upgrade wyngthon
```

---

## Next Step

After successfully installing the library, head over to [Quick Start](quick-start.md) to learn how to create your first client.
