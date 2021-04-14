#!/usr/bin/env python3

import discord
from discord import embeds
from discord.ext import commands
import praw # "python reddit api wrapper"
import json
import time
import extra
from sys import argv as cliargs

norepo = False
if("norepo" in cliargs):
	norepo = True

with open("tokenfile", "r") as tokenfile:
	token=tokenfile.read()

istatus = discord.Status.online
cstatus = discord.Game(name="reddit.com")

client = commands.Bot(status=istatus,activity=cstatus,command_prefix="~",help_command=extra.MyHelpCommand())
reddit = praw.Reddit("bot")

repomessage = discord.Embed(title="Repo",description="https://github.com/Vresod/reddit-bot")

@client.event
async def on_ready():
	print("logged in as {0.user}".format(client))

@client.event
async def on_guild_join(guild:discord.Guild):
	print(f"Joined guild: {guild.name}")


@client.command(aliases=["b"])
async def browse(ctx,sub,amount,listing):
		subreddit = reddit.subreddit(sub)
		if listing == "hot":
			listing = subreddit.hot
		elif listing == "top":
			listing = subreddit.top
		elif listing == "new":
			listing = subreddit.new
		elif listing == "random":
			listing = subreddit.random_rising
		elif listing == "rising":
			listing = subreddit.rising
		elif listing == "controversial":
			listing = subreddit.controversial
		stickiedposts = 0
		for stickytest in listing(limit=2):
			if(stickytest.stickied):
				stickiedposts += 1
		for submission in listing(limit=int(amount) + stickiedposts):
			if submission.is_self:
				if(len(submission.selftext) > 2048): # dealing with the limit on embedded text
					content = submission.selftext[:2045] + "..."
				else:
					content = submission.selftext
			else:
				content = submission.url
			if(submission.stickied):
				continue
			if(submission.over_18 and not ctx.channel.is_nsfw()):
				await ctx.send("NSFW post. Please try again in an NSFW channel.")
			else:
				if(len(submission.title) > 256): # title length limit
					sanitized_title = submission.title[:253] + "..."
				else:
					sanitized_title = submission.title
				temp_embed = discord.Embed(
					title=sanitized_title,
					url=submission.shortlink,
					color=discord.Color.from_rgb(255,127,0)
				)
				temp_embed.set_footer(text="posted by u/{0}".format(submission.author))
				if submission.is_self:
					temp_embed.description = content
				else:
					temp_embed.set_image(url=content)
				await ctx.send("{0} post from r/{1}:".format(listing.title(),submission.subreddit),embed=temp_embed)

@client.command()
async def repo(ctx):
	await ctx.send(embed=repomessage)

client.run(token)