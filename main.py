import os
import discord
from discord.ext import commands
from groq import Groq

TOKEN = os.getenv("TOKEN")
GROQ_KEY = os.getenv("GROQ_KEY")

client_ai = Groq(api_key=GROQ_KEY)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot online como {bot.user}")

@bot.command()
async def ia(ctx, *, pergunta):
    try:
        resposta = client_ai.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "Você é um assistente inteligente e amigável."},
                {"role": "user", "content": pergunta}
            ]
        )

        await ctx.send(resposta.choices[0].message.content)

    except Exception as e:
        await ctx.send("❌ Erro ao falar com a IA.")
        print(e)

bot.run(TOKEN)
