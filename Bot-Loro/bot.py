import discord
import os
import markovify
import subprocess
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

estado_personalidad = {
    "amable": 0.5,
    "bromista": 0.3,
    "grosero": 0.2
}

def build_model():
    carpeta = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(carpeta, "mis_palabras.txt")

    if not os.path.exists(ruta):
        return None

    mensajes = []
    with open(ruta, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if "|" in linea:
                contenido = linea.split("|", 1)[1].strip()
                if contenido:
                    mensajes.append(contenido)

    if not mensajes:
        return None

    texto = "\n".join(mensajes)
    return markovify.NewlineText(texto, state_size=1)


def actualizar_cpp(mensaje: str):
    carpeta = os.path.dirname(os.path.abspath(__file__))
    ejecutable = os.path.join(carpeta, "memoria")

    try:
        proceso = subprocess.Popen(
            [ejecutable],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=carpeta
        )
        salida, error = proceso.communicate(input=mensaje + "\n", timeout=5)

        for linea in salida.splitlines():
            if "AMABLE:" in linea:
                partes = linea.split()
                amable = float(partes[0].split(":")[1])
                bromista = float(partes[1].split(":")[1])
                grosero = float(partes[2].split(":")[1])
                return amable, bromista, grosero

        return 0.5, 0.3, 0.2

    except Exception as e:
        return 0.5, 0.3, 0.2


@bot.event
async def on_ready():
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

    amable, bromista, grosero = actualizar_cpp(message.content.strip())
    estado_personalidad["amable"] = amable
    estado_personalidad["bromista"] = bromista
    estado_personalidad["grosero"] = grosero


@bot.command()
async def hablar(ctx):
    model = build_model()
    if model is None:
        await ctx.send("Mi mochila de palabras está vacía. ¡Hablen más en el chat!")
        return

    sentence = model.make_sentence(tries=100, test_output=False)
    if not sentence:
        await ctx.send("Me quedé sin palabras...")
        return

    amable = estado_personalidad["amable"]
    bromista = estado_personalidad["bromista"]
    grosero = estado_personalidad["grosero"]

    if amable >= bromista and amable >= grosero:
        respuesta = f"{sentence} :3"
    elif bromista >= amable and bromista >= grosero:
        respuesta = f"{sentence} XDDD"
    else:
        respuesta = f"{sentence} >:c"

    await ctx.send(respuesta)


bot.run(TOKEN)
