import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

# 讀取 .env 檔案
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
        
        await self.tree.sync()
        print(f"Synced slash commands for {self.user}")

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

if __name__ == "__main__":
    if not TOKEN:
        print("錯誤：找不到 DISCORD_TOKEN。請確保 .env 檔案中設定了 Token。")
    else:
        bot = MyBot()
        bot.run(TOKEN)