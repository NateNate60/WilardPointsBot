import praw
import config
import authentication
import wpb as database
import time
import json

#Logs a message
def log(message: str) :
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + ": " + message)
    if config.logfile is not None :
        with open(config.path + "/" + config.logfile, 'a') as f :
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + ": " + message + '\n')

#Logs into Reddit, returning the Reddit instance
def login() :
    r = praw.Reddit(username=authentication.username,
                    password=authentication.password,
                    client_id=authentication.client_id,
                    client_secret=authentication.client_secret,
                    user_agent="WPB4")
    log('Authenticated')
    return r

#Process a list of PMs, looking for commands in them
def processinbox(r: praw.Reddit, accountsdb) :
    for message in r.inbox.unread() :
        r.inbox.mark_read([message])
        body = message.body.split()
        body[0] = body[0].lower()
        user = ''
        if "!bal" in body[0] :
            if len(body) == 2 and (not config.privatebalances or message.author.name in config.mods):
                user = body[1]
            else :
                user = message.author.name
            balance = database.balance(user, accountsdb)
            message.reply("User " + user + " has " + str(balance) + " " + config.currencyname + config.signature)
            log(message.author.name + " queried " + user +"'s balance, which is " + str(balance))
            continue
        if "!newa" in body[0] or "!createa" in body[0]:
            if database.balance(message.author.name) == None :
                database.createaccount(message.author.name, accountsdb, config.startingbalance)
                message.reply("Account created. Your starting balance is " + str(config.startingbalance) + " " + config.currencyname + config.signature)
                log(message.author.name + " created a new account")
            else :
                message.reply("You already have an account. Your balance is " + str(database.balance(message.author.name)) + " " + config.currencyname + config.signature)
            continue
        if ("!delete" in body[0] or "!close" in body[0]) and len(body) == 1 :
            if database.balance(message.author.name) == None :
                message.reply("You don't have an account." + config.signature)
            else :
                database.deleteaccount(message.author.name, accountsdb)
                message.reply("Your account has been deleted." + config.signature)
                log(message.author.name + " deleted their account")
            continue
        if "!trans" in body[0] or "!send" in body[0]:
            if len(body) < 3 :
                message.reply("Error: command `!transfer` takes 2 arguments, not " + str(len(body) - 1) + config.signature)
                continue
            if database.balance(message.author.name, accountsdb) == None :
                message.reply("You currently don't have an account. Run !newacc to create an account." + config.signature)
                continue
            if database.balance(body[1], accountsdb) == None :
                message.reply("The target user, " + body[1] + " does not have an account." + config.signature)
                continue
            try :
                amt = int(body[2])
                if amt <= 0 :
                    message.reply("Error: amount cannot be negative or zero" + config.signature)
                    continue
                if amt > database.balance(message.author.name, accountsdb) :
                    message.reply("Error: amount is greater than your available balance, which is " + str(database.balance(message.author.name, accountsdb)))
                    continue
                database.change(message.author.name, amt * -1, accountsdb)
                database.change(body[1], amt, accountsdb)
                message.reply("Transfer successful! Your available balance is now " + str(database.balance(message.author.name, accountsdb)) + " " + config.currencyname + config.signature)
                r.redditor(body[1]).message("You received a transfer", "You were sent " + str(amt) + " " + config.currencyname + " from u/" + message.author.name + config.signature)
                log(message.author.name + " transferred " + str(amt) + " to " + body[1] + "; new balance = " + str(database.balance(message.author.name, accountsdb)))
                continue
            except ValueError :
                message.reply("Error: amount must be an integer" + config.signature)
                continue
        mc = modcommand(message, accountsdb)
        if "!" in body[0] and not mc:
            message.reply("Command \"" + body[0] + "\" not found." + config.signature)
            if config.markread :
                continue
        if not mc :
            r.inbox.mark_unread([message])
    time.sleep(config.sleeptime)


#Check a message for mod commands. Returns true if a command was
# found and processed, false if no commands were found or the user
# is not a mod. This function returns true if a command was found, even if
# there was a syntax error in it
def modcommand(message, accountsdb) :
    body = message.body.split()
    reply = ""
    if message.author.name not in config.mods :
        return False
    if "!delete" in body[0] or "!close" in body[0] :
        for i in range(1,len(body)) :
            if database.balance(body[i], accountsdb) != None :
                database.deleteaccount(body[i], accountsdb)
                reply += "Successfully deleted " + body[i] +"'s account\n\n"
                log(message.author.name + " deleted " + body[i] + "'s account")
            else :
                reply += body[i] + " does not have an account\n\n"
        message.reply(reply + config.signature)
        return True
    if "!add" in body[0] or "!credit" in body[0] :
        if len(body) != 3 :
            message.reply("Error: `!credit` requires 2 arguments, not " + (len(body)-1) + config.signature)
            return True
        if database.balance(body[1], accountsdb) == None :
            message.reply("Error: user " + body[1] + " does not have an account" + config.signature)
            return True
        try :
            amt = int(body[2])
            database.change(body[1], amt, accountsdb)
            log(message.author.name + " changed " + body[1] + "'s balance by " + str(amt))
            message.reply("The command executed successfully. " + body[1] + " now has " + str(database.balance(body[1], accountsdb)) + " " + config.currencyname)
            return True
        except ValueError :
            message.reply("Error: \"" + body[2] +"\" is not an integer" + config.signature)
            return True
    if "!deduct" in body[0] or "!debit" in body[0] or "!dock" in body[0] or "!remove" in body[0] or "!subtract" in body[0]:
        if len(body) != 3 :
            message.reply("Error: `!debit` requires 2 arguments, not " + (len(body)-1) + config.signature)
            return True
        if database.balance(body[1], accountsdb) == None :
            message.reply("Error: user " + body[1] + " does not have an account" + config.signature)
            return True
        try :
            amt = int(body[2]) * -1
            if amt > 0 :
                amt *= -1
            database.change(body[1], amt, accountsdb)
            log(message.author.name + " changed " + body[1] + "'s balance by " + str(amt))
            message.reply("The command executed successfully. " + body[1] + " now has " + str(database.balance(body[1], accountsdb)) + " " + config.currencyname)
            return True
        except ValueError :
            message.reply("Error: \"" + body[2] +"\" is not an integer" + config.signature)
            return True
    return False

#Give points to top posts
def awardposts(r, accountsdb) :
    alreadycommented = []
    with open ('alreadycommented.json', 'r') as f :
        alreadycommented = json.load(f)
    if int(time.time())%21600 >= config.sleeptime :
        return alreadycommented
    for post in r.subreddit('townofsalemgame').hot(limit = 12) :
        if post.stickied or database.balance(post.author.name, accountsdb) == None or post.score < 80 :
            continue
        elif post.score >= config.tierscore[0] and post.score < config.tierscore[1] :
            tier = config.tier[0]
        elif post.score >= config.tierscore[1] and post.score < config.tierscore[2] :
            tier = config.tier[1]
        elif post.score >= config.tierscore[2] and post.score < config.tierscore[3] :
            tier = config.tier[2]
        elif post.score >= config.tierscore[3] and post.score < config.tierscore[4] :
            tier = config.tier[3]
        elif post.score >= config.tierscore[4] :
            tier = config.tier[4]
        award = post.score // 10
        database.change(post.author.name, award, accountsdb)
        log(post.author.name + " gained " + str(award) + " for post " + post.id)
        if post.id not in alreadycommented :
            post.reply ("Hello! I am the bot (that you subscribed to) that awards " + config.currencyname + " to good posts. I am pleased"+
                        " to inform you that your post has reached the " + tier + " tier. As such, I am awarding you " + str(award) + " " + config.currencyname + " for this post. I will update" +
                        " you if you earn more. I check the top 12 posts ever six hours. Pinned posts are unfortunately not eligible. You've got " + str(database.balance(post.author.name, accountsdb)) + " "  + config.currencyname + " now.")
            alreadycommented.append(post.id)
        else :
            post.author.message("Your account balance has increased","Your account balance has increased by " + str(award) + " " + config.currencyname + config.signature)
        with open('alreadycommented.json', 'w') as f :
            json.dump(alreadycommented)
