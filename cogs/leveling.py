import discord
import json
from discord import app_commands, ui
from discord.ext import commands

def load_users():
    try:
        with open('chat.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open('chat.json', 'w') as f:
        json.dump(users, f, indent=4)

async def create_leaderboard_embed(page: int, bot: commands.Bot, users):
    sorted_users = sorted(users.items(), key=lambda item: (item[1]['level'], item[1]['exp']), reverse=True)
    
    start_index = (page - 1) * 10
    end_index = start_index + 10
    
    embed = discord.Embed(title="💖 等級排行榜 💖", color=discord.Color.from_rgb(255, 170, 213))
    
    if start_index >= len(sorted_users):
        embed.description = "這一頁沒有資料呢！(｡>﹏<｡)"
    else:
        for i, (user_id, data) in enumerate(sorted_users[start_index:end_index], start=start_index + 1):
            try:
                user = await bot.fetch_user(int(user_id))
                embed.add_field(name=f"#{i} ✨ {user.display_name}", value=f"等級: {data['level']} | 經驗: {data['exp']}", inline=False)
            except discord.NotFound:
                embed.add_field(name=f"#{i} ❓ 未知的用戶 (ID: {user_id})", value=f"等級: {data['level']} | 經驗: {data['exp']}", inline=False)

    total_pages = (len(sorted_users) + 9) // 10
    embed.set_footer(text=f"頁數 {page}/{total_pages} (๑•̀ㅂ•́)و✧")
    return embed

class LeaderboardView(ui.View):
    def __init__(self, bot: commands.Bot, total_pages: int, initial_page: int = 1):
        super().__init__(timeout=180)
        self.bot = bot
        self.current_page = initial_page
        self.total_pages = total_pages
        self.update_buttons()

    def update_buttons(self):
        self.children[0].disabled = self.current_page == 1
        self.children[1].disabled = self.current_page == self.total_pages

    async def update_leaderboard(self, interaction: discord.Interaction):
        users = load_users()
        embed = await create_leaderboard_embed(self.current_page, self.bot, users)
        await interaction.response.edit_message(embed=embed, view=self)

    @ui.button(label="上一頁", style=discord.ButtonStyle.blurple)
    async def previous_button(self, interaction: discord.Interaction, button: ui.Button):
        self.current_page -= 1
        self.update_buttons()
        await self.update_leaderboard(interaction)

    @ui.button(label="下一頁", style=discord.ButtonStyle.blurple)
    async def next_button(self, interaction: discord.Interaction, button: ui.Button):
        self.current_page += 1
        self.update_buttons()
        await self.update_leaderboard(interaction)

class Leveling(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        users = load_users()
        user_id = str(message.author.id)
        if user_id not in users:
            users[user_id] = {
                "level": 1,
                "exp": 0
            }

        users[user_id]["exp"] += 5
        level = users[user_id]["level"]
        exp = users[user_id]["exp"]
        exp_to_next_level = level * 100

        if exp >= exp_to_next_level:
            users[user_id]["level"] += 1
            users[user_id]["exp"] = 0
            await message.channel.send(f"恭喜 {message.author.mention} 升到了 {users[user_id]['level']} 等！")

        save_users(users)

    @app_commands.command(name="rank", description="查看你的等級和經驗值")
    async def rank(self, interaction: discord.Interaction):
        users = load_users()
        user_id = str(interaction.user.id)
        if user_id in users:
            level = users[user_id]["level"]
            exp = users[user_id]["exp"]
            exp_to_next_level = level * 100
            
            sorted_users = sorted(users.items(), key=lambda item: (item[1]['level'], item[1]['exp']), reverse=True)
            rank_position = next((i + 1 for i, (uid, _) in enumerate(sorted_users) if uid == user_id), "N/A")

            embed = discord.Embed(
                title=f"✨ {interaction.user.display_name} 的等級資料 ✨",
                color=discord.Color.from_rgb(255, 170, 213)
            )
            embed.set_thumbnail(url=interaction.user.avatar.url)
            embed.add_field(name="💖 等級", value=f"**{level}**", inline=True)
            embed.add_field(name="🌟 經驗值", value=f"**{exp}/{exp_to_next_level}**", inline=True)
            embed.add_field(name="🏆 排行榜名次", value=f"**#{rank_position}**", inline=True)
            
            # Progress bar calculation
            progress = exp / exp_to_next_level
            filled_hearts = int(progress * 10)
            empty_hearts = 10 - filled_hearts
            progress_bar = "❤️" * filled_hearts + "🤍" * empty_hearts
            embed.add_field(name="進度", value=progress_bar, inline=False)
            
            embed.set_footer(text="繼續加油喔！(๑•̀ㅂ•́)و✧")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"你還沒有任何經驗值呢！(´;ω;`)")

    @app_commands.command(name="leaderboard", description="查看等級排行榜")
    async def leaderboard(self, interaction: discord.Interaction):
        users = load_users()
        sorted_users = sorted(users.items(), key=lambda item: (item[1]['level'], item[1]['exp']), reverse=True)
        total_pages = (len(sorted_users) + 9) // 10
        
        embed = await create_leaderboard_embed(1, self.bot, users)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        view = LeaderboardView(self.bot, total_pages, initial_page=1)
        
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(Leveling(bot))