import os
import base64
import discord
from discord.ext import commands
from openai import OpenAI

# ==============================
# CONFIGURAÇÕES
# ==============================

TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TOKEN:
    raise ValueError("DISCORD_TOKEN não configurado.")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY não configurado.")

client = OpenAI(api_key=OPENAI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ==============================
# EVENTOS
# ==============================

@bot.event
async def on_ready():
    print(f"✅ Bot online como {bot.user}")

# ==============================
# COMANDO DE IMAGEM
# ==============================

@bot.command()
async def img(ctx, *, prompt: str):
    await ctx.send("🎨 Gerando imagem... aguarde...")

    try:
        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )

        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        file_path = "generated.png"

        with open(file_path, "wb") as f:
            f.write(image_bytes)

        await ctx.send(file=discord.File(file_path))

        os.remove(file_path)

    except Exception as e:
        await ctx.send(f"❌ Erro ao gerar imagem:\n{e}")

# ==============================
# START
# ==============================

bot.run(TOKEN)
