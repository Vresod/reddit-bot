import discord
import praw # "python reddit api wrapper"
with open("tokenfile", "r") as tokenfile:
	token=tokenfile.read()
#print(token)

client = discord.Client()
reddit = praw.Reddit("bot")
prefix = "~"
helpmessage = discord.Embed(
	title="Bot Commands",
	description="~\{subreddit\} <limit> <listing> (Get posts from a subreddit)\n~bot (Shows this help message)",
	color=discord.Color.from_rgb(255, 127, 0)
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
	if message.content.startswith("{0}bot".format(prefix)):
		await message.channel.send(embed=helpmessage)
		return
	if message.content.startswith(prefix):
		args = message.content.replace(prefix,"")
		argslist = args.split(" ")
		print(argslist)
		subreddit = reddit.subreddit(argslist[0])
		print(subreddit)
		for submission in subreddit.hot(limit=int(argslist[1])):
			print("{0}\n{1}".format(submission.over_18,message.channel.is_nsfw()))
			if(submission.over_18 and not message.channel.is_nsfw()):
				await message.channel.send("NSFW post. Please try again in an NSFW channel.")
			else:
				await message.channel.send("Hot post from {0}: {1} {2}".format(subreddit,submission.title,submission.url))

client.run(token)