import discord
import random
import copy
from discord import app_commands, ui
from discord.ext import commands

# Emoji mapping for tile values
TILE_EMOJIS = {
    0: "▪️",
    2: "❤️",
    4: "🧡",
    8: "💛",
    16: "💚",
    32: "💙",
    64: "💜",
    128: "🖤",
    256: "🤍",
    512: "🟥",
    1024: "🟧",
    2048: "🟨",
    4096: "🟩",
    8192: "🟦",
    16384: "🟪",
    32768: "⬛",
    65536: "⬜"
}

# Legend to display below the board
EMOJI_LEGEND = "❤️2 🧡4 💛8 💚16 💙32 💜64 🖤128 🤍256\n🟥512 🟧1024 🟨2048 🟩4096..."

class Game2048:
    """Contains the logic for the 2048 game."""
    def __init__(self):
        self.grid = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.game_over = False
        self.add_new_tile()
        self.add_new_tile()

    def get_empty_cells(self):
        return [(r, c) for r in range(4) for c in range(4) if self.grid[r][c] == 0]

    def add_new_tile(self):
        empty_cells = self.get_empty_cells()
        if not empty_cells:
            return
        r, c = random.choice(empty_cells)
        self.grid[r][c] = 2 if random.random() < 0.9 else 4

    def compress(self, row):
        new_row = [i for i in row if i != 0]
        new_row += [0] * (4 - len(new_row))
        return new_row

    def merge(self, row):
        for i in range(3):
            if row[i] != 0 and row[i] == row[i+1]:
                row[i] *= 2
                self.score += row[i]
                row[i+1] = 0
        return row

    def move(self, direction):
        original_grid = copy.deepcopy(self.grid)
        
        if direction == 'left':
            for r in range(4):
                self.grid[r] = self.compress(self.merge(self.compress(self.grid[r])))
        
        elif direction == 'right':
            for r in range(4):
                reversed_row = self.grid[r][::-1]
                processed_row = self.compress(self.merge(self.compress(reversed_row)))
                self.grid[r] = processed_row[::-1]

        elif direction == 'up':
            self.grid = self.transpose(self.grid)
            self.move('left')
            self.grid = self.transpose(self.grid)

        elif direction == 'down':
            self.grid = self.transpose(self.grid)
            self.move('right')
            self.grid = self.transpose(self.grid)

        if self.grid != original_grid:
            self.add_new_tile()
            self.check_game_over()
            return True
        return False

    def transpose(self, grid):
        return [list(row) for row in zip(*grid)]

    def check_game_over(self):
        if self.get_empty_cells():
            self.game_over = False
            return

        for r in range(4):
            for c in range(4):
                if c < 3 and self.grid[r][c] == self.grid[r][c+1]:
                    self.game_over = False
                    return
                if r < 3 and self.grid[r][c] == self.grid[r+1][c]:
                    self.game_over = False
                    return
        self.game_over = True

class GameView(ui.View):
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot
        self.game = Game2048()

    def create_embed(self):
        board = "\n".join(" ".join(TILE_EMOJIS.get(cell, "❓") for cell in row) for row in self.game.grid)
        
        title = "💖 2048 小遊戲 💖"
        color = discord.Color.fuchsia()

        if self.game.game_over:
            title = "💔 遊戲結束 💔"
            color = discord.Color.dark_grey()

        embed = discord.Embed(title=title, description=f"**分數: {self.game.score}**\n\n{board}", color=color)
        embed.add_field(name="TILE KEY", value=EMOJI_LEGEND, inline=False)
        embed.set_footer(text="加油！(๑•̀ㅂ•́)و✧")
        return embed

    async def update_message(self, interaction: discord.Interaction):
        if self.game.game_over:
            for child in self.children:
                child.disabled = True
        
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    @ui.button(label="⬆️", style=discord.ButtonStyle.primary, row=0)
    async def up_button(self, interaction: discord.Interaction, button: ui.Button):
        self.game.move('up')
        await self.update_message(interaction)

    @ui.button(label="⬅️", style=discord.ButtonStyle.primary, row=1)
    async def left_button(self, interaction: discord.Interaction, button: ui.Button):
        self.game.move('left')
        await self.update_message(interaction)

    @ui.button(label="⬇️", style=discord.ButtonStyle.primary, row=1)
    async def down_button(self, interaction: discord.Interaction, button: ui.Button):
        self.game.move('down')
        await self.update_message(interaction)

    @ui.button(label="➡️", style=discord.ButtonStyle.primary, row=1)
    async def right_button(self, interaction: discord.Interaction, button: ui.Button):
        self.game.move('right')
        await self.update_message(interaction)
        
    @ui.button(label="結束遊戲", style=discord.ButtonStyle.danger, row=2)
    async def quit_button(self, interaction: discord.Interaction, button: ui.Button):
        self.game.game_over = True
        for child in self.children:
            child.disabled = True
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)
        self.stop()

class GameCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="2048", description="開始一場 2048 遊戲")
    async def play_2048(self, interaction: discord.Interaction):
        view = GameView(self.bot)
        embed = view.create_embed()
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(GameCog(bot))