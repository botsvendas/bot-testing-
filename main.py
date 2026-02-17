import os
import discord
from discord.ext import commands
from groq import Groq
import replicate

# ===== TOKENS =====
TOKEN = os.getenv("TOKEN")
GROQ_KEY = os.getenv("GROQ_KEY")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

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
# COMANDO GERAR IMAGEM
# ===============================
@bot.command()
async def img(ctx, *, prompt):
    try:
        await ctx.send("🎨 Gerando imagem... aguarde")

        output = replicate.run(
            "stability-ai/stable-diffusion-xl-base-1.0:latest",
            input={
                "prompt": prompt,
                "width": 1024,
                "height": 1024,
                "num_outputs": 1
            }
        )

        image_url = output[0]

        await ctx.send(image_url)

    except Exception as e:
        await ctx.send("❌ Erro ao gerar imagem.")
        print("ERRO IMG:", e)

bot.run(TOKEN)
