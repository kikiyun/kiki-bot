# Project Overview

This project is a Discord bot built with Python using the `discord.py` library. The bot is designed to be modular, with different categories of commands organized into separate files called "cogs".

## Core Features

*   **Command Handling:** The bot uses a `cogs` directory to manage its commands. Each file in this directory represents a category of commands.
*   **Leveling System:** The bot includes a leveling system that tracks user activity. Users gain experience points (XP) for sending messages and level up when they reach certain XP thresholds.
*   **Data Persistence:** User data for the leveling system is stored in `chat.json`.

## Architecture

The bot is structured as follows:

*   `bot.py`: The main entry point of the application. It initializes the bot, loads the cogs, and connects to Discord.
*   `cogs/`: A directory containing the bot's command modules (cogs).
    *   `basic.py`: Contains basic commands like `hello` and `echo`.
    *   `leveling.py`: Contains the logic for the leveling system, including the `rank` and `leaderboard` commands.
*   `chat.json`: A JSON file used to store user data for the leveling system.
*   `requirements.txt`: Lists the Python dependencies for the project.
*   `.env`: Stores environment variables, such as the Discord bot token.

# Building and Running

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Set Up Environment Variables:**
    Create a `.env` file in the root directory and add your Discord bot token:
    ```
    DISCORD_TOKEN=your_bot_token
    ```

3.  **Run the Bot:**
    ```bash
    python bot.py
    ```

# Development Conventions

*   **Modular Design:** Commands are organized into cogs to keep the codebase clean and maintainable.
*   **Data Handling:** The `leveling` cog handles its own data persistence by reading from and writing to `chat.json` on-demand.
*   **Asynchronous Programming:** The bot uses `asyncio` and `discord.py`'s asynchronous features to handle events and commands concurrently.
