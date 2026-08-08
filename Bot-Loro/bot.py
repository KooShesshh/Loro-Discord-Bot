import discord
import os
import markovify
import random
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

CORPUS_PATH = "textos.txt"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def ensure_corpus():
    if not os.path.exists(CORPUS_PATH):
        with open(CORPUS_PATH, "w", encoding="utf-8") as f:
            f.write("")


def build_model():
    ensure_corpus()
    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    if len(text.strip()) == 0:
        return None
    return markovify.NewlineText(text, state_size=1)


@bot.event
async def on_ready():
    ensure_corpus()
    print(f"Conectado como {bot.user}")


@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if message.author.bot:
        return
    if message.content.startswith("!"):
        return
    if len(message.content.split()) > 30:
        return
    if not message.content.strip():
        return

    with open(CORPUS_PATH, "a", encoding="utf-8") as f:
        f.write(message.content.strip() + "\n")


@bot.command()
async def hablar(ctx):
    model = build_model()
    if model is None:
        await ctx.send("Mi mochila de palabras está vacía. ¡Hablen más en el chat!")
        return

    sentence = model.make_sentence(tries=100, test_output=False)
    if sentence:
        await ctx.send(sentence)
    else:
        await ctx.send("Me quedé sin palabras...")


bot.run(TOKEN)
