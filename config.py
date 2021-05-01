
#Working directory for all the databases
#Must not end with '/'. So '/home/user/wpb' is OK,
# '/home/user/wpb/' is not OK
path = "/home/nate/wpb"

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
mods = ["MyUsername1", "MyUsername2"]

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

awardgoodposts = False


#When the bot checks for good posts to award points, what are the tiers of posts?
tier = ["FRAMER", "MAFIOSO", "BLACKMAILER", "CONSIGLIERE", "GODFATHER"]

#What are the required upvotes for the respective tiers?
tierscore = [80, 150, 300, 500, 1000]