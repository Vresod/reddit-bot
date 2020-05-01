
# Reddit Bot

This discord bot adds "commands" to discord to access reddit subreddits.

## Coding Style

Please use tabs, as opposed to spaces.

## How to use

Get a discord bot token and a reddit API token. Make the files "tokenfile" and "praw.ini".

- In tokenfile, put JUST the token and nothing else.

- In praw.ini, make it look similar to this.

```ini
[bot]
client_id=cLiEnTiDeNtItY
client_secret=fAKe-cLieNTseCrEtdoNOtsHare
user_agent=android:com.example.myredditapp:v1.2.3 (by u/kemitche)
```

You can learn about praw.ini [here](https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html).

Invite your bot to the discord server(s) of your choice and run the file.

Alternatively, you can just use [this](https://discordapp.com/api/oauth2/authorize?client_id=705130799082635345&permissions=0&scope=bot) pre-running bot that I use.

If you want to test the bot without inviting it, or get testing + development information, join [this](https://discord.gg/uEADNr) discord server.
