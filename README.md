# WilardPointsBot
A simple banking bot that can keep track of users' account balances and allows communities to create their own point/currency systems. Designed to work with Reddit via PRAW.

**This was one of my first projects, made while I was in secondary school. Please excuse the spaghetti code.**

## Installation

Download and unzip the source code. You can use [7-Zip](https://7-zip.org) for this on Windows, if you don't have a program to do this installed on your computer. 7-Zip is free and open-source software. 

Most Linux distributions have a pre-installed archiving tool (such as GNOME Archive Manager on Ubuntu), and you should use that.

**Automatic installation (recommended)** 

Simply run the built-in setup.py file and follow the instructions!

- Windows: `python setup.py`
- Mac and Linux: `python3 setup.py`

**Manual installation**

1. Copy all of the `.py` files to the desired location
2. Make a new file called "alreadycommented.json" with a single set of curly braces (`{}`) in it.
3. Make a new file called "config.py", and copy in the following contents:

```
#WILLARDPOINTSBOT CONFIG FILE 


#Working directory for all the databases
#Must not end with '/'. So '/home/user/wpb' is OK,
# '/home/user/wpb/' is not OK
path = /home/nate/wpb

#If a PM contains no suitable commands, should it be marked as read?
#Set to false if you have other scripts (or people) monitoring this
# inbox as well
markread = True

#How much does each user start with when they open an account?
startingbalance = 0

#What do you want your currency's name to be?
#Example: "Dopey Dingus Dollars", "USD", etc
currencyname = "WP"

#The signature is appended to the end of every one of the bot's
# comments and replies.
signature = "\n\n NateNate60's Willard Points Bot"

#Mods are approved users that can manually edit, add, or deduct from
# users' balances. Mod usernames should not be prefixed with "u/".
# This list is case-sensitive.
mods = ["NateNate60"]

#Should the bot log to a file? The bot always logs to stdout, but 
# by putting a file name here, you can log to a file as well. If
# you don't want to log to a file, set this to None
logfile = "log.txt"

#If set to true, then users cannot query another user's balance (but mods still can)
privatebalances = False

#If you're using the Reddit inbox checker, this is the interval in seconds
# that the bot waits between each time it checks its inbox. Setting this too
# low will result in problems with Reddit's rate limiter. Setting it higher
# will use less CPU time, but will mean a longer delay between receiving a command
# and the command being processed.
#This cannot be a negative number, but there is no limit to how high it can go.
sleeptime = 5



#####FREE POINT AWARDING#####

#This is a demonstration of the bot in action. You can set it to true to see how it works,  
# but by default, the bot does not give points away for free. If turned on, the bot checks
# every six hours for the top 12 posts in a subreddit and gives them points based on how
# many upvotes they have. The default settings are used in r/townofsalemgame.

awardgoodposts = True


#When the bot checks for good posts to award points, what are the tiers of posts?
tier = ["FRAMER", "MAFIOSO", "BLACKMAILER", "CONSIGLIERE", "GODFATHER"]

#What are the required upvotes for the respective tiers?
tierscore = [80, 150, 300, 500, 1000]

subreddit = "townofsalemgame"
```

4. Change the values in the config file to the settings you desire.
5. Install the Python Reddit API Wrapper:

- Windows: `pip install praw`
- Mac and Linux: `pip3 install praw`

That's it!

## Getting started

A ready-made bot is already coded into `main.py`. This bot will check its inbox for commands every five seconds, and give out free points to the top 12 posts in a given subreddit every six hours. You're highly encouraged to modify `main.py` to suit your own individual needs and what you want the bot to do.

The bot will automatically create the database of user accounts the first time it's run. The bot uses a SQLite database for this. 

Be sure to check out documentation.md for the documentation on the functionality included in the bot!
