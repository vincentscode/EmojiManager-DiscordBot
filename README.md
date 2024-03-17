# Emoji Manager Discord Bot
A simple Discord bot that allows users to manage custom emojis on a server.

## Usage
| Command | Description |
| ------- | ----------- |
| `/add_emojis <file>` | Parses the given TSV (`url name`) file and adds the emojis to the server. |
| `/emojis` | Lists all the emojis on the server as embeds. |

## Installation
1. Clone the repository.
2. Install the required packages using `pip install -r requirements.txt`.
3. Create a config.py file with the following content:
```python
class Configuration:
    token: str = None

    @classmethod
    def load(cls):
        instance = cls()
        instance.token = "YOUR_DISCORD_BOT_TOKEN"
        instance.testing_guild_ids = [1234567890]  # List of guild IDs where the bot should be active
        return instance
```
