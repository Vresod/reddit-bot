import discord
import praw # "python reddit api wrapper"
import json

with open("tokenfile", "r") as tokenfile:
	token=tokenfile.read()
with open("helpmessage.json", "r") as rawhelpmessage:
	jsonhelpmessage = json.loads(rawhelpmessage.read())
	print(jsonhelpmessage)
	jsonhelpmessage.help.strdescription = "\n".join(jsonhelpmessage.help.description)

client = discord.Client()
reddit = praw.Reddit("bot")
prefix = "~"
helpmessage = discord.Embed(
	title=jsonhelpmessage.help.title,
	description=jsonhelpmessage.help.strdescription,
	color=discord.Color.from_rgb(jsonhelpmessage.help.color)
)


@client.event
async def on_ready():
		print("logged in as {0.user}".format(client))

@client.event
async def on_message(message):
	if message.author == client.user or message.author.bot:
		return
	#if message.content.startswith("~wip"):
	#	await message.channel.send("This bot is a work in progress.")
	args = message.content.replace(prefix,"")
	argslist = args.split(" ")
	if message.content.startswith("{0}bot".format(prefix)):
		if(argslist[0] == help):
			await message.channel.send(embed=helpmessage)
		return
	if message.content.startswith(prefix):
		subreddit = reddit.subreddit(argslist[0])
		stickiedposts = 0
		for stickytest in subreddit.hot(limit=2):
			if(stickytest.stickied):
				stickiedposts += 1
		for submission in subreddit.hot(limit=int(argslist[1]) + stickiedposts):
			if(submission.stickied):
				continue
			if(submission.over_18 and not message.channel.is_nsfw()):
				await message.channel.send("NSFW post. Please try again in an NSFW channel.")
			else:
				await message.channel.send("Hot post from r/{0}: {1} {2}".format(subreddit,submission.title,submission.url))

client.run(token)