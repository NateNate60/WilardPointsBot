#import reddit
import wpb as database
import reddit
import config

def main() :
    accountsdb = database.opendb()
    r = reddit.login()
    while True :
        inbox = reddit.checkinbox()
        reddit.processinbox(r, inbox, accountsdb)
        reddit.awardposts(r, alreadycommented, accountsdb)