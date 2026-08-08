# Loro-Discord-Bot

Hi i am Koo, this is a vibe-coded discord bot in python

**How to use this bot**

This is a simple Discord bot that listens to what people say in the chat, remembers the words, and can later generate random sentences that sound a bit like the server’s usual talking style. It’s basically a digital parrot with a short memory.

### What you need

- Python 3.8 or higher  
- A Discord bot token (you create this yourself in the Discord Developer Portal)  
- The following Python packages: `discord.py`, `markovify`, `python-dotenv`

You can install the packages with:

```bash
pip install discord.py markovify python-dotenv
```

### Setup

1. Clone or download this repository.
2. Create a file named `.env` in the same folder as the bot and put your token inside:

```
DISCORD_TOKEN=your_token_here
```

3. Invite the bot to your server with the proper permissions (at least “Send Messages” and “Read Message History”).
4. Run the bot:

```bash
python bot.py
```

If everything is correct, you’ll see a message in the terminal saying the bot is online.

### How it works

- Just talk normally in any channel the bot can see. It quietly saves short messages (up to 30 words) to a local file called `textos.txt`.
- When you want the bot to say something, type:

```
!hablar
```

It will try to generate a sentence based on everything it has heard so far. The more people talk, the better (and weirder) the results usually get.

### A few notes

- The bot ignores messages that start with `!` so it doesn’t learn its own commands.
- It also ignores messages from other bots and very long messages.
- The first few times you use `!hablar` the results might be empty or nonsense. That’s normal — it needs some chat history to work with.
- The file `textos.txt` is created automatically. You can delete it if you ever want the bot to start learning from scratch.

That’s pretty much it. Let it hang out in the chat for a while and then make it talk.
