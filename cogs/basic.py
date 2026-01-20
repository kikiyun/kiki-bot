import random
from discord import app_commands
from discord.ext import commands

class Basic(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="hello", description="打聲招呼！")
    async def hello(self, interaction):
        greetings = [
            f"你好，{interaction.user.mention}！",
            f"嗨，{interaction.user.mention}！很高興見到你！",
            f"哈囉，{interaction.user.mention}！今天過得如何？",
            f"安安，{interaction.user.mention}！",
            f"Yo，{interaction.user.mention}！"
        ]
        await interaction.response.send_message(random.choice(greetings))

    @app_commands.command(name="echo", description="重複你說的話")
    @app_commands.describe(message="要重複的話")
    async def echo(self, interaction, message: str):
        await interaction.response.send_message(f"你說了：{message}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Basic(bot))