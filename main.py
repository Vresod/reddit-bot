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
if(not file_exists("./runtime/prefixes.json")):
	with open("./runtime/prefixes.json","w") as tempprefixfile:
		tempprefixfile.write("{}")
with open("./runtime/prefixes.json","r") as rawprefixes:
	prefixes = json.loads(rawprefixes.read())

client = discord.Client()
reddit = praw.Reddit("bot")
helpmessage = discord.Embed(
	title=jsonhelpmessage["help"]["title"],
	description=jsonhelpmessage["help"]["strdescription"],
	color=discord.Color.from_rgb(jsonhelpmessage["help"]["color"][0],jsonhelpmessage["help"]["color"][1],jsonhelpmessage["help"]["color"][2])
)
prefixsuccessmessage = discord.Embed(
	title=jsonhelpmessage["prefix_success"]["title"],
	description=jsonhelpmessage["prefix_success"]["strdescription"],
	color=discord.Color.from_rgb(jsonhelpmessage["prefix_success"]["color"][0],jsonhelpmessage["prefix_success"]["color"][1],jsonhelpmessage["prefix_success"]["color"][2])
)
prefixfailuremessage = discord.Embed(
	title=jsonhelpmessage["prefix_failure"]["title"],
	description=jsonhelpmessage["prefix_failure"]["strdescription"],
	color=discord.Color.from_rgb(jsonhelpmessage["prefix_failure"]["color"][0],jsonhelpmessage["prefix_failure"]["color"][1],jsonhelpmessage["prefix_failure"]["color"][2])
)

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
				if submission.is_self:
					await message.channel.send("Hot post from r/{0}:".format(subreddit),embed=discord.Embed(title="{0}".format(submission.title),description="{0}".format(content)))
				else:
					await message.channel.send("Hot post from r/{0}: `{1}`\n{2}".format(subreddit,submission.title,content))

client.run(token)