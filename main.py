#!/usr/bin/env python3

import asyncprawcore
import discord
from discord import embeds
from discord.ext import commands
import asyncpraw as praw # "python reddit api wrapper"
import extra
import sys
from sys import argv as cliargs
import traceback

norepo = False
if("norepo" in cliargs):
	norepo = True

with open("tokenfile", "r") as tokenfile:
	token=tokenfile.read()

cstatus = discord.Game(name="reddit.com")

client = commands.Bot(activity=cstatus,command_prefix="~",help_command=extra.MyHelpCommand())
reddit = praw.Reddit("bot")

repomessage = discord.Embed(title="Repo",description="https://github.com/Vresod/reddit-bot")
acceptable_file_exts = (".png",".gif",".jpeg",".jpg",".webp")

@client.event
async def on_ready():
	print(f"logged in as {client.user}")

@client.event
async def on_guild_join(guild:discord.Guild):
	print(f"Joined guild: {guild.name}")

@client.event
async def on_command_error(ctx:commands.Context, exception):
	embed = discord.Embed(color=discord.Color.red())
	if type(exception) is commands.errors.MissingRequiredArgument:
		embed.title = "You forgot an argument"
		embed.description = f"The syntax to `{client.command_prefix}{ctx.invoked_with}` is `{client.command_prefix}{ctx.invoked_with} {ctx.command.signature}`."
		await ctx.send(embed=embed)
	elif type(exception) is commands.CommandNotFound:
		embed.title = "Invalid command"
		embed.description = f"The command you just tried to use is invalid. Use `{client.command_prefix}help` to see all commands."
		await ctx.send(embed=embed)
	elif type(exception) is commands.errors.NotOwner:
		app_info = await client.application_info()
		embed.title = "You do not have access to this command."
		embed.description = f"You must be the owner of this discord bot ({app_info.owner.name})."
		await ctx.send(embed=embed)
	else:
		print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
		traceback.print_exception(type(exception), exception, exception.__traceback__, file=sys.stderr)

@client.command(aliases=["b"],brief="browse subreddit")
async def browse(ctx,sub,amount = 5,listing = "hot"):
		amount = int(amount)
		if amount > 30:
			await ctx.send("you are over the limit of 30 posts. try doing less.")
			return
		subreddit = await reddit.subreddit(sub)
		try:
			async for _ in subreddit.hot(limit=1): pass
		except asyncprawcore.exceptions.NotFound:
			await ctx.send(embed=discord.Embed(title="Subreddit not found!",description="The subreddit you are searching for could not be found."))
			return
		if listing == "hot":
			listing_cl = subreddit.hot
		elif listing == "top":
			listing_cl = subreddit.top
		elif listing == "new":
			listing_cl = subreddit.new
		elif listing == "random":
			listing_cl = subreddit.random_rising
		elif listing == "rising":
			listing_cl = subreddit.rising
		elif listing == "controversial":
			listing_cl = subreddit.controversial
		stickiedposts = 0
		async for stickytest in listing_cl(limit=2):
			if(stickytest.stickied):
				stickiedposts += 1
		async for submission in listing_cl(limit=amount + stickiedposts):
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
			else: # the only situation in which the post gets posted
				if(len(submission.title) > 256): # title length limit
					sanitized_title = submission.title[:253] + "..."
				else:
					sanitized_title = submission.title
				if not submission.is_self and not submission.url.endswith(acceptable_file_exts): # if its not an image that can be read by discord
					await ctx.send("{0} post from r/{1}:\n```\n{2}\n```\n{3}".format(listing.title(),submission.subreddit,sanitized_title,submission.url))
					continue
				temp_embed = discord.Embed(
					title=sanitized_title,
					url=submission.shortlink,
					color=discord.Color.from_rgb(255,127,0)
				)
				temp_embed.set_footer(text=f"posted by u/{submission.author}")
				if submission.is_self:
					temp_embed.description = content
				else:
					temp_embed.set_image(url=content)
				await ctx.send(f"{listing.title()} post from r/{submission.subreddit()}:",embed=temp_embed)


@client.command(brief="show github repo")
async def repo(ctx):
	await ctx.send(embed=repomessage)

client.run(token)