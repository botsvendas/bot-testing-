import os
import discord
from discord.ext import commands
from groq import Groq
import requests
import time

# ===== TOKENS =====
TOKEN = os.getenv("TOKEN")
GROQ_KEY = os.getenv("GROQ_KEY")
HORDE_KEY = os.getenv("STABLE_HORDE_KEY")

# ===== IA TEXTO (Groq) =====
client_ai = Groq(api_key=GROQ_KEY)

# ===== DISCORD =====
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot online como {bot.user}")

# ===============================
# COMANDO IA TEXTO
# ===============================
@bot.command()
async def ia(ctx, *, pergunta):
    try:
        resposta = client_ai.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Você é um assistente inteligente e amigável."},
                {"role": "user", "content": pergunta}
            ]
        )
        await ctx.send(resposta.choices[0].message.content)
    except Exception as e:
        await ctx.send("❌ Erro ao falar com a IA.")
        print("ERRO IA:", e)

# ===============================
# COMANDO GERAR IMAGEM (Stable Horde)
# ===============================
@bot.command()
async def img(ctx, *, prompt):
    try:
        await ctx.send("🎨 Gerando imagem... pode demorar um pouco")

        headers = {
            "apikey": HORDE_KEY,
            "Content-Type": "application/json"
        }

        data = {
            "prompt": prompt,
            "params": {
                "width": 512,
                "height": 512,
                "steps": 25
            }
        }

        # Envia pedido
        response = requests.post(
            "https://stablehorde.net/api/v2/generate/async",
            headers=headers,
            json=data
        )

        request_id = response.json()["id"]

        # Espera imagem ficar pronta
        while True:
            check = requests.get(
                f"https://stablehorde.net/api/v2/generate/status/{request_id}",
                headers=headers
            ).json()

            if check["done"]:
                image_url = check["generations"][0]["img"]
                await ctx.send(image_url)
                break

            time.sleep(3)

    except Exception as e:
        await ctx.send("❌ Erro ao gerar imagem.")
        print("ERRO IMG:", e)

bot.run(TOKEN)
