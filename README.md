# Dragon Discord Bot

Dragon Discord Bot is an engaging, interactive bot for Discord servers, allowing users to hatch, grow, and battle with their own virtual dragons. It combines elements of RPGs and virtual pets, providing a unique, immersive experience for Discord communities.

## Features

- **Dragon Hatching:** Users can hatch their own dragon, giving it a unique name.
- **Growth and Development:** Feed and nurture your dragon using items found during adventures.
- **Battles:** Engage in dragon battles, either against dungeon monsters or PvP combat, to gain experience and improve your dragon's stats.
- **Inventory Management:** Collect items and manage your inventory to support your dragon's growth and combat abilities.
- **Leaderboards:** Compete with other players for a spot on the server's leaderboard based on your dragon's level and achievements.

## Setup

1. **Clone the repository:**
 ```bashgit clone https://github.com/bodanLabs/discord_dragons_rpg_bot.git ```
2. **Install dependencies:**
Ensure you have Python 3.8 or newer and pip installed. Then, navigate to the bot directory and install the required Python packages:
```cd dragon-discord-bot```
```pip install -r requirements.txt```
3. **Configuration:**
Rename config.json.example to config.json and fill in your Discord bot token and other relevant configurations.
4. **Database Setup:**
```python setup_database.py```

## Usage

- Start the bot:
```python bot.py```
- Bot Commands:
!hatch <dragonName>: Hatch your dragon.
!feed <item> <amount>: Feed your dragon to gain XP.
!fight @user <amount>: Challenge another user to a dragon fight.
!inventory: Check your current inventory.
!leaderboard: View the server's dragon leaderboard.
Additional commands and details can be found by using !help in Discord.

## Contributing
Contributions to the Dragon Discord Bot are welcome! If you have an idea for a feature or notice a bug, please open an issue. If you'd like to contribute code, please fork the repository, make your changes, and submit a pull request.
