# Loro-Discord-Bot

Discord bot with an evolving personality and memory engine written in C++.

## Features

- Receives chat messages and stores them
- Personality that changes based on the language used (kind, jokester, rude)
- Sentence generation with Markovify using the real message history
- Response style adapts to the current personality

## Requirements

- Python 3.10+
- `discord.py`
- `markovify`
- `python-dotenv`
- C++ compiler (`g++`)

## Installation

1. Clone the repository
2. Create a virtual environment and install the dependencies:

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
# or
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

3. Create a `.env` file with your token:

```
DISCORD_TOKEN=your_token_here
```

4. Compile the C++ engine:

```bash
g++ memoria.cpp -o memoria
```

The `memoria` executable must be in the same folder as `bot.py`.

## Usage

```bash
python bot.py
```

Commands:
- `!hablar` → the bot generates a sentence based on the history and its current personality

## Structure

- `bot.py` → Discord bot (Python)
- `memoria.cpp` → memory and personality engine (C++)
- `mis_palabras.txt` → message history (generated automatically)
- `personalidad.txt` → personality state (generated automatically)

## Notes

The `.txt` files are created automatically and are **not** uploaded to the repository.
