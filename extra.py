# needed for is_real_subreddit()
import praw
reddit = praw.Reddit("bot")

# i dont know what to name this. i need an equivalent to function(args){return args} in javascript
def test_if_can_be_converted_to_int(integer_as_string):
	try:
		int(integer_as_string)
		return True
	except:
		return False
# uses praw errors to check for real subs
def is_real_subreddit(unknown_subreddit):
	try:
		for submission in reddit.subreddit(unknown_subreddit).hot(limit=1):
			submission.title
		return True
	except:
		return False
# a large-ish function that i didn't want in the main file.
def get_sanitized(argumentlist):
	if(
		(len(argumentlist) == 2 or len(argumentlist) == 3) and
		(
			(len(argumentlist) == 2 and argumentlist[0] + argumentlist[1] == "bothelp") or
			(len(argumentlist) == 2 and argumentlist[0] + argumentlist[1] == "botrepo") or
			(len(argumentlist) == 3 and argumentlist[0] + argumentlist[1] == "botprefix") or
			(len(argumentlist) == 3 and is_real_subreddit(argumentlist[0]) and test_if_can_be_converted_to_int(argumentlist[1]))
		)
	):
		return True
	else:
		return False
# needed to make runtime/prefixes.json if it doesn't exist, like first time runs
def file_exists(path):
	try:
		with open(path,"r") as x:
			x.read()
			return True
	except:
		return False
# determine if a dictionary contains a thing
def dictionary_contains(dictionary, thing):
	try:
		dictionary[str(thing)]
		return True
	except:
		return False