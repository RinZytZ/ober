import os
import discord
from discord.ext import commands
import asyncio
from datetime import timedelta

TOKEN = os.getenv("API_TOKEN")
PREFIX = "!"

# Запрещённые подстроки (мутит, если они ЕСТЬ в сообщении)
bad_words = ["ронз", "нз", "бег", "nz", "чел", "chel", "run", "67"]

# Режим контроля
control_mode = {}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

def is_admin(ctx):
    return ctx.author.guild_permissions.administrator

def contains_bad_word(text):
    """Возвращает True, если любая запрещённая подстрока есть в тексте"""
    text_lower = text.lower()
    for word in bad_words:
        if word in text_lower:
            return True
    return False

@bot.event
async def on_ready():
    print(f"🪖 {bot.user} готов к обороне!")
    print(f"Запрещённых подстрок: {bad_words}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.guild is None:
        return
    
    # Режим контроля
    if control_mode.get(str(message.guild.id), False):
        should_delete = False
        
        if message.flags.crossposted or message.type == discord.MessageType.forward:
            should_delete = True
        
        if message.attachments:
            should_delete = True
        
        if message.embeds:
            should_delete = True
        
        if should_delete:
            try:
                await message.delete()
                print(f"☂️ Удалено (режим контроля): {message.author.name} -> {message.content}")
            except:
                pass
            return
    
    # Проверка на запрещённые подстроки
    if contains_bad_word(message.content):
        try:
            await message.author.timeout(timedelta(minutes=1), reason="Запрещённая подстрока")
            await message.delete()
            print(f"🪖 ЗАМУТИЛ {message.author.name} за: {message.content}")
        except Exception as e:
            print(f"Ошибка мута: {e}")
        return
    
    await bot.process_commands(message)

@bot.command(name="отзовись")
async def respond(ctx):
    if not is_admin(ctx):
        return
    await ctx.send("Так точно!")

@bot.command(name="добавить_слово")
async def add_word(ctx, *, word: str):
    if not is_admin(ctx):
        return
    
    word_lower = word.lower()
    if word_lower not in bad_words:
        bad_words.append(word_lower)
        await ctx.send(f"🪖 Подстрока `{word_lower}` добавлена в список")

@bot.command(name="удалить_слово")
async def remove_word(ctx, *, word: str):
    if not is_admin(ctx):
        return
    
    word_lower = word.lower()
    if word_lower in bad_words:
        bad_words.remove(word_lower)
        await ctx.send(f"🪖 Подстрока `{word_lower}` удалена из списка")

@bot.command(name="список_слов")
async def list_words(ctx):
    if not is_admin(ctx):
        return
    
    if bad_words:
        await ctx.send(f"🪖 Запрещённые подстроки: {', '.join(bad_words)}")
    else:
        await ctx.send("🪖 Список пуст")

@bot.command(name="контроль")
async def toggle_control(ctx):
    if not is_admin(ctx):
        return
    
    guild_id = str(ctx.guild.id)
    new_state = not control_mode.get(guild_id, False)
    control_mode[guild_id] = new_state
    
    if new_state:
        await ctx.send("🪖 **ACHTUNG!** Режим контроля активирован!\nВсе пересылки, гифки, фото и видео будут уничтожены.\nFeindliche Nachrichten werden eliminiert!")
    else:
        await ctx.send("🪖 Режим контроля деактивирован. Возвращаемся к обычной обороне.")

@bot.command(name="статус")
async def status(ctx):
    if not is_admin(ctx):
        return
    
    mode = "ВКЛЮЧЁН" if control_mode.get(str(ctx.guild.id), False) else "ВЫКЛЮЧЁН"
    await ctx.send(f"🪖 Режим контроля: {mode}\n🪖 Подстрок в списке: {len(bad_words)}")

async def main():
    while True:
        try:
            async with bot:
                await bot.start(TOKEN)
        except Exception as e:
            print(f"🪖 Ошибка: {e}")
            import traceback
            traceback.print_exc()
            print("Перезапуск через 5 секунд...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
