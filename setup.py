
def main() :
    print ("--Willard Points Bot setup--")
    try:
        import sys
        import subprocess
        import os
        import shutil
        import sqlite3
    except ModuleNotFoundError:
        print ("You are missing required system packages. Setup cannot install WillardPointsBot automatically.")
        print ("This may be due to a corrupt or inadequate Python installation")
        print ("You can still install WillardPointsBot manually.")
        return 1
    try:
        import praw
    except ModuleNotFoundError:
        print ("It appears that the Python Reddit API Wrapper is not installed on your system.")
        print ("Setup can automatically install PRAW for you.")
        ok = input("Would you like to automatically install PRAW? (y/n): ")
        if "y" in ok :
            if "win" in sys.platform :
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'praw'])
            else :
                subprocess.check_call([sys.executable, '-m', 'pip3', 'install', 'praw'])
        else :
            print ("PRAW will not be installed. The Reddit integration of WPB will not work without PRAW.")
    path = ''
    while True :
        path = input("Enter the path to the directory you'd like to install the files in (press enter to install in current directory): ")
        if path == "" :
            path = "."
        if path[0] == "~" :
            path = path [1:]
            path = os.path.expanduser('~') + path
        path = os.path.realpath(path)
        print("WillardPointsBot will be installed in", path)
        ok = input("Is this correct? (y/n): ")
        if 'y' in ok or ok == '':
            break
    try:
        os.mkdir(path)
    except FileExistsError:
        print ("WARNING: folder already exists and might not be empty!")
        input ("Press enter to continue, or press Control + C to quit")
    with open (path + '/config.py', 'w') as f:
        w = "#WILLARDPOINTSBOT CONFIG FILE \n\n\n\n#Working directory for all the databases\n#Must not end with '/'. So '/home/user/wpb' is OK,\n# '/home/user/wpb/' is not OK\n"
        w += "path = " + path + '\n\n'
        w += "#If a PM contains no suitable commands, should it be marked as read?\n#Set to false if you have other scripts (or people) monitoring this\n# inbox as well\nmarkread = True\n\n#How much does each user start with when they open an account?\nstartingbalance = 0\n\n#What do you want your currency's name to be?\n#Example: \"Dopey Dingus Dollars\", \"USD\", etc\ncurrencyname = \"WP\"\n\n#The signature is appended to the end of every one of the bot's\n# comments and replies.\nsignature = \"\\n\\n NateNate60's Willard Points Bot\"\n\n#Mods are approved users that can manually edit, add, or deduct from\n# users' balances. Mod usernames should not be prefixed with \"u/\".\n# This list is case-sensitive.\nmods = [\"MyUsername1\", \"MyUsername2\"]\n\n#Should the bot log to a file? The bot always logs to stdout, but \n# by putting a file name here, you can log to a file as well. If\n# you don't want to log to a file, set this to None\nlogfile = \"log.txt\"\n\n#If set to true, then users cannot query another user's balance (but mods still can)\nprivatebalances = False\n\n#If you're using the Reddit inbox checker, this is the interval in seconds\n# that the bot waits between each time it checks its inbox. Setting this too\n# low will result in problems with Reddit's rate limiter. Setting it higher\n# will use less CPU time, but will mean a longer delay between receiving a command\n# and the command being processed.\n#This cannot be a negative number, but there is no limit to how high it can go.\nsleeptime = 5\n\n\n\n#####FREE POINT AWARDING#####\n\n#This is a demonstration of the bot in action. You can set it to true to see how it works,  \n# but by default, the bot does not give points away for free. If turned on, the bot checks\n# every six hours for the top 12 posts in a subreddit and gives them points based on how\n# many upvotes they have. The default settings are used in r/townofsalemgame.\n\nawardgoodposts = False\n\n\n#When the bot checks for good posts to award points, what are the tiers of posts?\ntier = [\"FRAMER\", \"MAFIOSO\", \"BLACKMAILER\", \"CONSIGLIERE\", \"GODFATHER\"]\n\n#What are the required upvotes for the respective tiers?\ntierscore = [80, 150, 300, 500, 1000]\n\nWhich subreddit should the bot check for posts? Leave out the r/\nsubreddit = \"mysubreddit\""
        f.write(w)
    with open (path + '/' + 'alreadycommented.json', 'w') as f:
        f.write("{}")
    with open (path + "/log.txt", 'w') as f:
        f.write("This is the WPB debug logfile. If you enabled logging to file in the config (located at " + path + "), output will be logged here. Log to file is on by default")
    shutil.copyfile("./reddit.py", path + '/reddit.py')
    shutil.copyfile("./main.py", path + '/main.py')
    shutil.copyfile("./wpb.py", path + "/wpb.py")
    print ("Installation complete!")
    print ("To use WPB, simply import the Python modules located at \"" + path + "\". Refer to the documentation for more information: https://github.com/NateNate60/WilardPointsBot/blob/master/README.md")
    print ("There is a demonstration version of the bot available at " + path + "/main.py. It is highly recommended that you put the rest of your bot's files in " + path + " as well.")
    return 0
if __name__ == '__main__' :
    main()