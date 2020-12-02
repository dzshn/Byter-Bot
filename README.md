# Byter-Bot

Source code for the Discord bot made for the Créu Cat community

---

## Running
While I suggest you to **not** have a fork running, it's good to do testing on code if you want to contribute, so below is the steps to how to run this code

### requirements
* Python 3.6 or higher
* [discord.py](https://github.com/Rapptz/discord.py)
* [psutil](https://github.com/giampaolo/psutil)
* [py-googletrans](https://github.com/ssut/py-googletrans) (optional, for translator only)

Create a `config.py` file as following:
```py
prefixes = []
```
as well as a `TOKEN` file, contaning only the bot token

then, simply run the `main.py` script