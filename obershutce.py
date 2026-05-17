import discord
from discord.ext import commands
import random
import asyncio
import os

TOKEN = os.getenv("API_TOKEN")
ADMIN_ID = 991057181677850694

# Запрещённые слова
FORBIDDEN_WORDS = ["ронз", "нз", "бег", "nz", "чел", "chel", "run", "67"]

# Фразы для уебков (вместо удаления с 50% шансом)
REPLY_PHRASES = [
    "Очень сука смешно урод",
    "Иди нахуй, пес",
    "Ты ебанутый?",
    "Завали ебало",
    "Очередной даун",
    "В рот ебал"
]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🪖 {bot.user} — готов!")

@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return
    
    if message.guild is None:
        return
    
    content_lower = message.content.lower()
    has_forbidden = any(word in content_lower for word in FORBIDDEN_WORDS)
    
    if has_forbidden:
        # 50% удаляем, 50% отвечаем фразой
        if random.random() < 0.5:
            await message.delete()
            print(f"Удалено от {message.author.name}")
        else:
            phrase = random.choice(REPLY_PHRASES)
            await message.channel.send(f"🪖 {message.author.mention}, {phrase}")
    
    await bot.process_commands(message)

# Простые команды
@bot.command(name="отзовись")
async def respond(ctx):
    if ctx.author.guild_permissions.administrator:
        await ctx.send("Так точно!")

@bot.command(name="добавить_слово")
async def add_word(ctx, *, word: str):
    if ctx.author.guild_permissions.administrator:
        word_lower = word.lower()
        if word_lower not in FORBIDDEN_WORDS:
            FORBIDDEN_WORDS.append(word_lower)

@bot.command(name="удалить_слово")
async def remove_word(ctx, *, word: str):
    if ctx.author.guild_permissions.administrator:
        word_lower = word.lower()
        if word_lower in FORBIDDEN_WORDS:
            FORBIDDEN_WORDS.remove(word_lower)

@bot.command(name="список_слов")
async def list_words(ctx):
    if ctx.author.guild_permissions.administrator:
        await ctx.send(f"🪖 Слова: {', '.join(FORBIDDEN_WORDS)}")

bot.run(TOKEN)
