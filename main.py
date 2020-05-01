import discord
import praw # "python reddit api wrapper"
import json

def file_exists(path):
	try:
		with open(path,"r") as x:
			x.read()
			return True
	except:
		return False

with open("tokenfile", "r") as tokenfile:
	token=tokenfile.read()
with open("helpmessage.json", "r") as rawhelpmessage:
	jsonhelpmessage = json.loads(rawhelpmessage.read())
	jsonhelpmessage["help"]["strdescription"] = "\n".join(jsonhelpmessage["help"]["description"])
	jsonhelpmessage["prefix_success"]["strdescription"] = "\n".join(jsonhelpmessage["prefix_success"]["description"])
	jsonhelpmessage["prefix_failure"]["strdescription"] = "\n".join(jsonhelpmessage["prefix_failure"]["description"])
	jsonhelpmessage["repo"]["strdescription"] = "\n".join(jsonhelpmessage["repo"]["description"])
if(not file_exists("./runtime/prefixes.json")):
	with open("./runtime/prefixes.json","w") as tempprefixfile:
		tempprefixfile.write("{}")
with open("./runtime/prefixes.json","r") as rawprefixes:
	prefixes = json.loads(rawprefixes.read())

client = discord.Client()
reddit = praw.Reddit("bot")

helpmessage = discord.Embed(title=jsonhelpmessage["help"]["title"],description=jsonhelpmessage["help"]["strdescription"],color=discord.Color.from_rgb(jsonhelpmessage["default_color"][0],jsonhelpmessage["default_color"][1],jsonhelpmessage["default_color"][2]))
prefixsuccessmessage = discord.Embed(title=jsonhelpmessage["prefix_success"]["title"],description=jsonhelpmessage["prefix_success"]["strdescription"],color=discord.Color.from_rgb(jsonhelpmessage["default_color"][0],jsonhelpmessage["default_color"][1],jsonhelpmessage["default_color"][2]))
prefixfailuremessage = discord.Embed(title=jsonhelpmessage["prefix_failure"]["title"],description=jsonhelpmessage["prefix_failure"]["strdescription"],color=discord.Color.from_rgb(jsonhelpmessage["default_color"][0],jsonhelpmessage["default_color"][1],jsonhelpmessage["default_color"][2]))
repomessage = discord.Embed(title=jsonhelpmessage["repo"]["title"],description=jsonhelpmessage["repo"]["strdescription"],color=discord.Color.from_rgb(jsonhelpmessage["default_color"][0],jsonhelpmessage["default_color"][1],jsonhelpmessage["default_color"][2]))

@client.event
async def on_guild_join(server):
	prefixes[server.id] = "~"
	prefixesfile = open("./runtime/prefixes.json", "w")
	prefixesfile.write(json.dumps(prefixes))
	prefixesfile.close()

@client.event
async def on_ready():
		print("logged in as {0.user}".format(client))

@client.event
async def on_message(message):
	if message.author == client.user or message.author.bot:
		return
	if not message.content.startswith(prefixes[str(message.guild.id)]):
		return
	args = message.content.replace(prefixes[str(message.guild.id)],"")
	argslist = args.split(" ")
	if message.content.startswith("{0}bot".format(prefixes[str(message.guild.id)])):
		if(argslist[1] == "help"):
			await message.channel.send(embed=helpmessage)
		if(argslist[1] == "prefix"):
			if(not message.author.permissions_in(message.channel).manage_guild):
				await message.channel.send(embed=prefixfailuremessage)
				return
			prefixes[str(message.guild.id)] = argslist[2]
			await message.channel.send(embed=prefixsuccessmessage)
			prefixesfile = open("./runtime/prefixes.json", "w")
			prefixesfile.write(json.dumps(prefixes))
			prefixesfile.close()
		if(argslist[1] == "repo"):
			await message.channel.send(embed=repomessage)
		return
	if message.content.startswith(prefixes[str(message.guild.id)]):
		subreddit = reddit.subreddit(argslist[0])
		stickiedposts = 0
		for stickytest in subreddit.hot(limit=2):
			if(stickytest.stickied):
				stickiedposts += 1
		for submission in subreddit.hot(limit=int(argslist[1]) + stickiedposts):
			if submission.is_self:
				content = submission.selftext
			else:
				content = submission.url
			if(submission.stickied):
				continue
			if(submission.over_18 and not message.channel.is_nsfw()):
				await message.channel.send("NSFW post. Please try again in an NSFW channel.")
			else:
				temp_embed = discord.Embed(
					title=submission.title,
					url=submission.shortlink,
					color=discord.Color.from_rgb(jsonhelpmessage["default_color"][0],jsonhelpmessage["default_color"][1],jsonhelpmessage["default_color"][2])
				)
				if submission.is_self:
					temp_embed.description = content
				else:
					temp_embed.set_image(url=content)
				await message.channel.send("Hot post from r/{0}:".format(subreddit),embed=temp_embed)

client.run(token)