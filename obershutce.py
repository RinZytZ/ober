import os
import discord
import json
from datetime import datetime, timedelta

TOKEN = os.getenv("API_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

# ===== НАСТРОЙКИ =====
bad_words = ["ронз", "нз", "бег", "nz", "чел", "chel", "run", "67"]
control_mode = {}
CONTROL_FILE = "control_mode.json"

# Загружаем режим контроля
if os.path.exists(CONTROL_FILE):
    with open(CONTROL_FILE, "r", encoding="utf-8") as f:
        control_mode = json.load(f)

def save_control_mode():
    with open(CONTROL_FILE, "w", encoding="utf-8") as f:
        json.dump(control_mode, f, ensure_ascii=False, indent=2)

# ===== СОБЫТИЯ =====
@client.event
async def on_ready():
    print(f"🪖 Обершутце активирован: {client.user}")
    print(f"Запрещённых слов: {bad_words}")
    print(f"Режим контроля активен на: {list(control_mode.keys())}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.guild is None:
        return
    
    # ===== РЕЖИМ КОНТРОЛЯ =====
    if control_mode.get(str(message.guild.id), False):
        is_plain_text = (
            not message.attachments and
            not message.embeds and
            not message.flags.crossposted and
            message.type == discord.MessageType.default
        )
        
        if not is_plain_text:
            try:
                await message.delete()
                print(f"☂️ Удалено (контроль) от {message.author.name}")
            except:
                pass
            return
    
    # ===== ОБРАБОТКА КОМАНД =====
    if not message.content.startswith("!"):
        # Обычное сообщение — проверка на запрещённые слова
        for word in bad_words:
            if word in message.content.lower():
                try:
                    await message.author.timeout(discord.utils.timedelta(minutes=1))
                    await message.delete()
                    print(f"🪖 Мут {message.author.name} за: {word}")
                except:
                    pass
                break
        return
    
    # Разбор команд
    cmd = message.content[1:].lower().split()[0] if message.content[1:] else ""
    args = message.content[1:].split()[1:] if len(message.content[1:].split()) > 1 else []
    
    # ===== !отзовись =====
    if cmd == "отзовись":
        if message.author.guild_permissions.administrator:
            await message.channel.send("Так точно!")
    
    # ===== !добавить_слово =====
    elif cmd == "добавить_слово":
        if message.author.guild_permissions.administrator and args:
            word = args[0].lower()
            if word not in bad_words:
                bad_words.append(word)
                await message.channel.send(f"🪖 Слово `{word}` добавлено")
    
    # ===== !удалить_слово =====
    elif cmd == "удалить_слово":
        if message.author.guild_permissions.administrator and args:
            word = args[0].lower()
            if word in bad_words:
                bad_words.remove(word)
                await message.channel.send(f"🪖 Слово `{word}` удалено")
    
    # ===== !список_слов =====
    elif cmd == "список_слов":
        if message.author.guild_permissions.administrator:
            await message.channel.send(f"🪖 Запрещённые слова: {', '.join(bad_words)}")
    
    # ===== !контроль =====
    elif cmd == "контроль":
        if message.author.guild_permissions.administrator:
            guild_id = str(message.guild.id)
            control_mode[guild_id] = not control_mode.get(guild_id, False)
            save_control_mode()
            
            if control_mode[guild_id]:
                await message.channel.send("🪖 **ACHTUNG!** Режим контроля активирован!\nВсе пересылки, картинки, гифки, видео и ссылки будут уничтожены.")
            else:
                await message.channel.send("🪖 Режим контроля деактивирован.")
    
    # ===== !статус =====
    elif cmd == "статус":
        if message.author.guild_permissions.administrator:
            mode = "ВКЛЮЧЁН" if control_mode.get(str(message.guild.id), False) else "ВЫКЛЮЧЁН"
            await message.channel.send(f"🪖 Режим контроля: {mode}\n🪖 Слов в списке: {len(bad_words)}")

# ===== ЗАПУСК =====
if __name__ == "__main__":
    client.run(TOKEN)
