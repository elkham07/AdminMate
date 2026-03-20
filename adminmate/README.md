# AdminMate - Discord Moderation & Utility Bot

AdminMate is a multifunctional Discord bot written in Python using the `discord.py` library. The bot is designed for automatic moderation, member activity tracking, an XP/leveling system, and providing weekly automated server digests.

## 🚀 Key Features

* **XP & Leveling System**: Members earn experience points (XP) for sending messages. Upon reaching a new level, the bot sends a congratulatory notification.
* **Anti-Spam Protection**: The bot automatically deletes links (`http://`, `https://`, `discord.gg`) posted by users who have been on the server for fewer than 7 days.
* **Support Ticket System**: Members can quickly open private ticket channels to communicate with server administrators using the `!ticket` command.
* **Auto-Digest**: The bot automatically tracks weekly statistics (total messages, new member count, most active channel, most active member) and publishes a beautiful report every Sunday at 9 AM UTC. Administrators can also manually trigger the digest using `!digest`.
* **Moderation suite**: Built-in commands for kick, ban, chat purging (clear), and warnings (`warn`). If a user receives 3 warnings, they are automatically kicked from the server.
* **Welcome Messages**: The bot greets every new member upon joining the server in the designated general channel.

## 🛠️ Setup & Installation

### 1. Requirements

To run this bot, you will need:
* Python 3.8 or newer
* Discord API Token

### 2. Environment Configuration

Create a `.env` file in the root folder of the project (`adminmate`) and add your Discord bot token:

```env
DISCORD_TOKEN
```

### 3. Install Dependencies

Install the required libraries using pip:

```bash
pip install discord python-dotenv
```

*(Note for macOS users: If you encounter SSL certificate verification errors during API requests, ensure you run the `Install Certificates.command` provided with your Python installation or update the `certifi` module).*

### 4. Running the Bot

Start the bot from your terminal:

```bash
python3 bot.py
```

##  Available Commands

### General Commands:
* `!level [user]` — Displays the current level and XP of a user (or yourself if left blank).
* `!ticket [problem description]` — Creates a private text channel (ticket) to contact moderators.
* `!close` — Closes and deletes the current ticket channel (only works within a ticket channel).

### Moderation Commands (permissions required):
* `!warn <user> [reason]` — Issues a warning to a member. Reaching 3 warnings results in an auto-kick.
* `!clear [amount]` — Deletes a specified number of messages in the channel (default is 10).
* `!kick <user> [reason]` — Kicks a member from the server.
* `!ban <user> [reason]` — Bans a member from the server.
* `!digest` — Manually triggers the server digest report.

##  Data Structure

The bot relies on local JSON files to persistently store data between reboots:
* `xp.json` — Stores XP and current levels for all server members.
* `warns.json` — Stores the warning history of members.

*Note: The `digest_messages` and `new_members` structures are cached in memory for the weekly digest and will reset upon automated posting.*

---

