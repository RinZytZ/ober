import discord
from discord.ext import commands
import random
import asyncio
import os
import logging
from datetime import timedelta

# ЗАТКНИ ЛОГИ
logging.getLogger('discord').setLevel(logging.CRITICAL)
logging.getLogger('discord.gateway').setLevel(logging.CRITICAL)

TOKEN = os.getenv("API_TOKEN")
ADMIN_ID = 991057181677850694  # Твой ID, The Deep

PREFIX = "хоум-"

# Запрещённые слова
FORBIDDEN_WORDS = ["ронз", "нз", "бег", "nz", "чел", "chel", "run", "67"]

# Фразы Хоумлендера
REPLY_PHRASES = [
    "Ты никто.",
    "Заткнись, уебок.",
    "Я спасаю мир, а ты пишешь эту хуйню.",
    "Ещё слово — и ты полетишь с крыши.",
    "Я бог. Ты — мусор.",
    "Vought заплатит за твою риторику? Нет? Тогда иди нахуй.",
    "Твоё мнение ничего не значит.",
    "Ты слаб. Как и все вы.",
    "Я всё вижу. И ты мне не нравишься.",
    "Жалкий уебок, даже The Deep и то полезнее.",
    "А ну цдалил нахуй а то переебашу тут всех"
]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

def is_admin(ctx):
    return ctx.author.id == ADMIN_ID

@bot.event
async def on_ready():
    print(f"🇺🇸 {bot.user} — Хоумлендер в деле. Префикс: {PREFIX}")

@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return
    
    if message.guild is None:
        return
    
    content_lower = message.content.lower()
    has_forbidden = any(word in content_lower for word in FORBIDDEN_WORDS)
    
    if has_forbidden:
        try:
            await message.author.timeout(timedelta(minutes=1), reason="Запрещённое слово")
        except:
            pass
        
        if random.random() < 0.5:
            await message.delete()
        else:
            phrase = random.choice(REPLY_PHRASES)
            await message.channel.send(f"🇺🇸 **{message.author.mention}**\n{phrase}")
    
    await bot.process_commands(message)

# ===== КОМАНДЫ ТОЛЬКО ДЛЯ ТЕБЯ (THE DEEP) =====
@bot.command(name="отзовись")
async def respond(ctx):
    if not is_admin(ctx):
        return
    await ctx.send("🇺🇸 Я здесь. Всегда. А ты, The Deep, иди корми рыб.")

@bot.command(name="добавить_слово")
async def add_word(ctx, *, word: str):
    if not is_admin(ctx):
        return
    word_lower = word.lower()
    if word_lower not in FORBIDDEN_WORDS:
        FORBIDDEN_WORDS.append(word_lower)
        await ctx.send(f"🇺🇸 Слово `{word_lower}` добавлено.")

@bot.command(name="удалить_слово")
async def remove_word(ctx, *, word: str):
    if not is_admin(ctx):
        return
    word_lower = word.lower()
    if word_lower in FORBIDDEN_WORDS:
        FORBIDDEN_WORDS.remove(word_lower)
        await ctx.send(f"🇺🇸 Слово `{word_lower}` удалено.")

@bot.command(name="список_слов")
async def list_words(ctx):
    if not is_admin(ctx):
        return
    await ctx.send(f"🇺🇸 Запрещённые слова: {', '.join(FORBIDDEN_WORDS)}")

bot.run(TOKEN)
