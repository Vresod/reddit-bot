#!/usr/bin/env python3

import discord
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
with open("helpmessage.json", "r") as rawhelpmessage:
	jsonhelpmessage = json.loads(rawhelpmessage.read())
	jsonhelpmessage["help"]["strdescription"] = "\n".join(jsonhelpmessage["help"]["description"])
	jsonhelpmessage["prefix_success"]["strdescription"] = "\n".join(jsonhelpmessage["prefix_success"]["description"])
	jsonhelpmessage["prefix_failure"]["strdescription"] = "\n".join(jsonhelpmessage["prefix_failure"]["description"])
	jsonhelpmessage["repo"]["strdescription"] = "\n".join(jsonhelpmessage["repo"]["description"])
	jsonhelpmessage["prefix_directmessage"]["strdescription"] = "\n".join(jsonhelpmessage["prefix_directmessage"]["description"])

with open("./runtime/prefixes.json","r") as rawprefixes:
	prefixes = json.loads(rawprefixes.read())

istatus = discord.Status.online
cstatus = discord.Game(name="reddit.com")


client = discord.Client(status=istatus,activity=cstatus)
reddit = praw.Reddit("bot")

helpmessage = discord.Embed(title=jsonhelpmessage["help"]["title"],description=jsonhelpmessage["help"]["strdescription"],color=discord.Color.from_rgb(jsonhelpmessage["default_color"][0],jsonhelpmessage["default_color"][1],jsonhelpmessage["default_color"][2]))
prefixsuccessmessage = discord.Embed(title=jsonhelpmessage["prefix_success"]["title"],description=jsonhelpmessage["prefix_success"]["strdescription"],color=discord.Color.from_rgb(jsonhelpmessage["default_color"][0],jsonhelpmessage["default_color"][1],jsonhelpmessage["default_color"][2]))
prefixfailuremessage = discord.Embed(title=jsonhelpmessage["prefix_failure"]["title"],description=jsonhelpmessage["prefix_failure"]["strdescription"],color=discord.Color.from_rgb(jsonhelpmessage["default_color"][0],jsonhelpmessage["default_color"][1],jsonhelpmessage["default_color"][2]))
repomessage = discord.Embed(title=jsonhelpmessage["repo"]["title"],description=jsonhelpmessage["repo"]["strdescription"],color=discord.Color.from_rgb(jsonhelpmessage["default_color"][0],jsonhelpmessage["default_color"][1],jsonhelpmessage["default_color"][2]))
prefixdirectmessage = discord.Embed(title=jsonhelpmessage["prefix_directmessage"]["title"],description=jsonhelpmessage["prefix_directmessage"]["strdescription"],color=discord.Color.from_rgb(jsonhelpmessage["default_color"][0],jsonhelpmessage["default_color"][1],jsonhelpmessage["default_color"][2]))


@client.event
async def on_ready():
	print("logged in as {0.user}".format(client))

@client.event
async def on_message(message):
	if message.author == client.user or message.author.bot:
		return
	serverprefix = ""
	if (message.guild != None):
		if(extra.dictionary_contains(prefixes, str(message.guild.id))):
			serverprefix = prefixes[str(message.guild.id)]
		else:
			serverprefix = "~"
	else:
		serverprefix = "~"
	if not message.content.startswith(serverprefix):
		return
	args = message.content.replace(serverprefix,"") # args is everything after the prefix
	argslist = args.split(" ") # gets args as a list. obviously.
	#if(not extra.get_sanitized(argslist)): # see extra.py
	#	#await message.channel.send("Your message could not be processed. Make sure you're following the rules defined in `{0}bot help`".format(serverprefix))
	#	return
	if message.content.startswith("{0}bot".format(serverprefix)):
		if(argslist[1] == "help"):
			await message.channel.send(embed=helpmessage)
		elif(argslist[1] == "prefix"):
			if (message.guild != None):
				if(not message.author.permissions_in(message.channel).manage_guild):
					await message.channel.send(embed=prefixfailuremessage)
				prefixes[str(message.guild.id)] = argslist[2]
				prefixesfile = open("./runtime/prefixes.json", "w")
				prefixesfile.write(json.dumps(prefixes))
				prefixesfile.close()
				await message.channel.send(embed=prefixsuccessmessage)
			else:
				await message.channel.send(embed=prefixdirectmessage)
		elif(argslist[1] == "repo" and not norepo):
			await message.channel.send(embed=repomessage)
		return
	if message.content.startswith(serverprefix):
		print(serverprefix)
		subreddit = reddit.subreddit(argslist[0])
		listing = ""
		if argslist[2] == "hot":
			listing = subreddit.hot
		if argslist[2] == "top":
			listing = subreddit.top
		if argslist[2] == "new":
			listing = subreddit.new
		if argslist[2] == "random":
			listing = subreddit.random_rising
		if argslist[2] == "rising":
			listing = subreddit.rising
		if argslist[2] == "controversial":
			listing = subreddit.controversial
		stickiedposts = 0
		for stickytest in listing(limit=2):
			if(stickytest.stickied):
				stickiedposts += 1
		for submission in listing(limit=int(argslist[1]) + stickiedposts):
			if submission.is_self:
				if(len(submission.selftext) > 2048): # dealing with the limit on embedded text
					content = submission.selftext[:2045] + "..."
				else:
					content = submission.selftext
			else:
				content = submission.url
			if(submission.stickied):
				continue
			if(submission.over_18 and not message.channel.is_nsfw()):
				await message.channel.send("NSFW post. Please try again in an NSFW channel.")
			else:
				if(len(submission.title) > 256): # title length limit
					sanitized_title = submission.title[:253] + "..."
				else:
					sanitized_title = submission.title
				temp_embed = discord.Embed(
					title=sanitized_title,
					url=submission.shortlink,
					color=discord.Color.from_rgb(jsonhelpmessage["default_color"][0],jsonhelpmessage["default_color"][1],jsonhelpmessage["default_color"][2])
				)
				temp_embed.set_footer(text="posted by u/{0}".format(submission.author))
				if submission.is_self:
					temp_embed.description = content
				else:
					temp_embed.set_image(url=content)
				await message.channel.send("{0} post from r/{1}:".format(argslist[2].title(),submission.subreddit),embed=temp_embed)
				time.sleep(0.5)

client.run(token)