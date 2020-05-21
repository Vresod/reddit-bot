
# Reddit Bot

[![Join the chat at https://gitter.im/reddit-bot/community](https://badges.gitter.im/reddit-bot/community.svg)](https://gitter.im/reddit-bot/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

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

If you want to test the bot without inviting it, or get testing + development information, join [this](https://discord.gg/yjr7mNA) discord server.

## Notes

To server owners: if someone says to invite the bot, make sure that you either trust the version of the bot that they have or that it's the official version of the bot. If the bot on your server is custom, it could have devastating consequences for the server. This applies to any discord bot, not just mine.

I do not recommend setting the prefix to nothing, or "". You can't do it, even. If you NEED to have the prefix set to nothing, use a version prior to [`8bf94a0`](https://github.com/Vresod/reddit-bot/commit/8bf94a0cbc4bab4bc57c6b8ea46e8ee3f27b2e7e). If you don't, it will tell you that you formatted your command wrong every time someone sends a message.
