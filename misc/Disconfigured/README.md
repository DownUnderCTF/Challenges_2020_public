# Disconfigured

**Category:** Misc

**Difficulty:** Medium

**Discord:** Delta#5000

**CTFd description:** I hope someone told the admins that this bot is for notes and not secrets.
Who knows what they might be hiding 👀

---
\
**Admin Notes**:
### **Summary**
Discord bot that is misconfigured as public, which means that users can invite it to their own servers.

The bot has admin commands that allow the dumping of arbitrary mongo collections. The flag will be stored in the DUCTF discord server collection.

### **Important Information**
When used in the DUCTF server, it should only register commands in the #bot-challenge server, otherwise it should tell the invoker to use that channel.
It will delete all messages sent in #bot-challenge.
I've tried to make it operate inside dm's as much as possible, please let me know if you notice it is misbehaving.

Ideally for ease of use it should have server admin perms, but really it just needs to be able to read & send in the relevant channels as well as delete messages in the host server.

#### **Prefix**
The bot prefix can be changed in .env.
It defaults to `!`

### **Deploy**
`docker-compose up -d`