import discord
from discord.ext import commands
import random
import asyncio
import os
from datetime import timedelta

TOKEN = os.getenv("API_TOKEN")

# Запрещённые слова
FORBIDDEN_WORDS = ["ронз", "нз", "бег", "nz", "чел", "chel", "run", "67"]

# Фразы Хоумлендера (высокомерно, пафосно, жестоко)
REPLY_PHRASES = [
    "Ты никто.",
    "Заткнись, уебок.",
    "Ты серьезно? Я спасаю мир, а ты пишешь эту хуйню.",
    "Ещё слово — и ты полетишь с крыши.",
    "Я бог. Ты — мусор.",
    "Vought заплатит за твою риторику? Нет? Тогда иди нахуй.",
    "Твоё мнение ничего не значит.",
    "Ты слаб. Как и все вы.",
    "Я всё вижу. И ты мне не нравишься.",
    "Ещё одна такая хуйня — и ты исчезнешь."
]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🇺🇸 {bot.user} — Я — Хоумлендер. И я здесь, чтобы навести порядок.")

@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return
    
    if message.guild is None:
        return
    
    content_lower = message.content.lower()
    has_forbidden = any(word in content_lower for word in FORBIDDEN_WORDS)
    
    if has_forbidden:
        # Мут на 1 минуту
        try:
            await message.author.timeout(timedelta(minutes=1), reason="Запрещённое слово")
        except:
            pass
        
        # 50% удаляем, 50% отвечаем фразой Хоумлендера
        if random.random() < 0.5:
            await message.delete()
            print(f"Удалено и замучено от {message.author.name}")
        else:
            phrase = random.choice(REPLY_PHRASES)
            await message.channel.send(f"🇺🇸 **{message.author.mention}**\n{phrase}")
            print(f"Хоумлендер уничтожил {message.author.name}")
    
    await bot.process_commands(message)

# Команды
@bot.command(name="отзовись")
async def respond(ctx):
    if ctx.author.guild_permissions.administrator:
        await ctx.send("🇺🇸 Я здесь. Всегда.")

@bot.command(name="добавить_слово")
async def add_word(ctx, *, word: str):
    if ctx.author.guild_permissions.administrator:
        word_lower = word.lower()
        if word_lower not in FORBIDDEN_WORDS:
            FORBIDDEN_WORDS.append(word_lower)
            await ctx.send(f"🇺🇸 Слово `{word_lower}` добавлено в чёрный список.")

@bot.command(name="удалить_слово")
async def remove_word(ctx, *, word: str):
    if ctx.author.guild_permissions.administrator:
        word_lower = word.lower()
        if word_lower in FORBIDDEN_WORDS:
            FORBIDDEN_WORDS.remove(word_lower)
            await ctx.send(f"🇺🇸 Слово `{word_lower}` удалено.")

@bot.command(name="список_слов")
async def list_words(ctx):
    if ctx.author.guild_permissions.administrator:
        await ctx.send(f"🇺🇸 Запрещённые слова: {', '.join(FORBIDDEN_WORDS)}")

bot.run(TOKEN)
