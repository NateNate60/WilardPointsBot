# Function documentation

## wpb.py

---

<br/>

##  `function opendb( )`
Return: sqlite3 database object

Opens an existing database, `accounts.sqlite3`. If the database doesn't exist, then it will create a new database in the working directory as specified in the config file.

## `function deleteaccount(user: str, accountsdb)`
Return: nothing

`accountsdb` is the database object.

Delete a user account as identified by that user's username. That user's entry in the account database will be deleted. Note that this function does not accept a `redditor` object from PRAW. You must fetch that user's username using `redditor.name` and pass that into this function.

This will delete MyUser's account:

    deleteaccount("MyUser", accountsdb)

## `function createaccount(user: str, accountsdb, startingbalance=config.startingbalance)`
Return: nothing

`accountsdb` is the database object.

Create an account under the username `user`, with the starting balance `startingbalance`. If `startingbalance` is not specified, then the default specified in the config file will be used.

This will create a new account for the user "myuser" with a balance of 5:

    wpb.createaccount("myuser", accountsdb, 5)

## `function change(user: str, amount: int, accountsdb)`
Return: nothing

Add or remove `amount` from `user`'s account.
`accountsdb` is the database object.

This will remove 5 from MyUser's balance:

    wpb.change("MyUser", -5, accountsdb)

...and this will _add_ 5 to MyUser's balance:

    wpb.change("MyUser", 5, accountsdb)

## `function balance(user: str, accountsdb=None)`
Return: `user`'s balance (`int`)

Fetch a user's balance. `accountsdb` is the database object. If `accountsdb` is not provided, then this function will open `accounts.sqlite3` and look in there. If the user does not have an account, then this returns `None`. Therefore, this function can also be used to check if a user has an account or not.

This function can be called with only the `user` parameter.

## reddit.py
---

<br/>

## `function log(message: str)`
Return: nothing

Log a message to stdout and to file (if specified in config). This will append the human-readable time before the message, to improve readability.

## `function login( )`
Return: PRAW Reddit instance

Logs into Reddit using the authentication information provided in `authentication.py`.

## `function processinbox(r: praw.Reddit, accountsdb)`
Return: nothing

Process commands in the inbox of the bot (unread only). It will first check for normal user commands, then for moderator commands.

Messages containing actual commands will be marked as read once processed. Messages not containing commands will be marked as read if specified in the config.

## `function modcommand(message, accountsdb)`
Return: whether any commands were found, regardless of whether they succeeded (`bool`)

`accountsdb` is the database object. `message` is a PRAW private message object, comment object, or post object. It is not recommended you pass posts into this function.

Processes a message for any mod commands. Returns `False` if the author of the message isn't on the list of mods (as specified in the config), or if no valid commands were found. Returns `True` if a valid command was detected (regardless of whether the command succeeded).

## `function awardposts(r: praw.Reddit, accountsdb)`
Return: nothing

`accountsdb` is the database object. `r` is the PRAW Reddit instance.

This function checks the top 12 posts in Hot of the subreddit specified in the config. If they have more than 80 upvotes, *and they have an account with the bot*, then they will earn one free point for every 10 upvotes. They will get a comment the first time their post earns free points, then they will get a PM about it every time thereafter.

The "tier" of the post is determined by between which thresholds (specified in config) the post's upvote count falls between. The tier is the respective entry in the tier list (also in config).