#import reddit
import wpb as database
import reddit
import config

def main() :
    accountsdb = database.opendb()
    r = reddit.login()
    while True :
        reddit.processinbox(r, accountsdb)
        reddit.awardposts(r, accountsdb)

main()