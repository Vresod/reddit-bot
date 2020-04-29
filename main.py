import discord
import praw # "python reddit api wrapper"

with open("tokenfile", "r") as tokenfile:
	token=tokenfile.read()
print(token)

client = discord.Client()

@client.event
async def on_ready():
		print("logged in as {0.user}".format(client))
		status = discord.CustomActivity(name="browsing reddit")
		await client.change_presence(activity=status, afk=False, status=discord.Status.online)

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	if message.content.startswith("~wip"):
		await message.channel.send("This bot is a work in progress.")
	

client.run(token)