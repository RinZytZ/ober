import discord
from discord.ext import commands
import asyncio
from datetime import timedelta

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = "обер-"

# Запрещённые слова (базовый список, редактируй прямо здесь)
bad_words = ["ронз", "нз", "бег", "nz", "чел", "chel", "run", "67"]

# Режим контроля: {guild_id: True/False}
control_mode = {}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

def is_admin(ctx):
    return ctx.author.guild_permissions.administrator

@bot.event
async def on_ready():
    print(f"🪖 {bot.user} готов к обороне!")
    print(f"Запрещённых слов: {len(bad_words)}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.guild is None:
        return
    
    # ===== РЕЖИМ КОНТРОЛЯ =====
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
            except:
                pass
            return
    
    # ===== ПРОВЕРКА НА ЗАПРЕЩЁННЫЕ СЛОВА =====
    content_lower = message.content.lower()
    for word in bad_words:
        if word in content_lower:
            try:
                await message.author.timeout(timedelta(minutes=1), reason=f"Запрещённое слово: {word}")
                await message.delete()
            except:
                pass
            break
    
    await bot.process_commands(message)

# ===== КОМАНДЫ =====
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

@bot.command(name="удалить_слово")
async def remove_word(ctx, *, word: str):
    if not is_admin(ctx):
        return
    
    word_lower = word.lower()
    if word_lower in bad_words:
        bad_words.remove(word_lower)

@bot.command(name="список_слов")
async def list_words(ctx):
    if not is_admin(ctx):
        return
    
    if bad_words:
        await ctx.send(f"🪖 Запрещённые слова: {', '.join(bad_words)}")
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
    await ctx.send(f"🪖 Режим контроля: {mode}\n🪖 Слов в списке: {len(bad_words)}")

# ===== АВТОПЕРЕЗАПУСК =====
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