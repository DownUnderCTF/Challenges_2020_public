require('dotenv').config();
const Discord = require('discord.js');
const bot = new Discord.Client();
const Bucket = require("./bucket.js")
const Parser = require("./parse.js")
const prompts = require('prompts')


async function main() {
  // Not apart of the challenge pls don't try and hack the bot :(
  const TOKEN = process.env.TOKEN || await getToken();
  bot.login(TOKEN);
}

async function getToken() {
  const token = await prompts( {
    type: 'text',
    name: 'token',
    message: 'Please enter bot token'
  })
  return token.token;
}

// apparently we use this bucket for ONLY memes now smh
// const memeBucketName = "secure-epic-meme" 
const memeBucketName = "epic-meme1"

const parser = Parser.parser;


bot.on('ready', () => {
  console.info(`Logged in as ${bot.user.tag}!`);
});

bot.on( 'message', async(msg) => {
    if (msg.author.bot) return;
    if (msg.channel.type !== "dm") return;
    if (Date.now() <  new Date("2020-09-18T19:00:10.000Z").getTime()) {
      msg.channel.send("Memes will be served when the CTF starts :)");
      return;
    }


    console.log(`Message: ${msg.content}`)
    const words = msg.content.split(" ");
    if (words[0] === "!meme") {
        words.shift();
        let argv;
        try {
            argv = parser.parseArgs(words);
        } catch (e) {
            msg.channel.send("You send a message I couldn't understand")
            msg.channel.send(e);
            return;
        }

        // LIST COMMAND
        if (argv.subcommand_name === 'list') {
            msg.channel.send("Memes that are available for consumption are:")
            try {
              const memeList = await  Bucket.getListOfMemes(memeBucketName);
              const toSend = memeList.map(meme => "➡ " + meme).join("\n");
              msg.channel.send(toSend)
            } catch(e) {
              console.error(e)
              msg.channel.send("⚠Looks like there was an error listing your memes :( maybe try again later?⚠")
            }
            
        }


        // GET COMMAND
        if (argv.subcommand_name === "get") {
            if (!(argv.meme || argv.signed_url)) {
                // Print usage
                msg.channel.send(Parser.getCmd.formatHelp())
                return;
            }

            if (argv.meme) {
                // Get meme from bucket
                msg.channel.send("Getting meme ...");

                try {
                  const url = await Bucket.generateSignedURL(memeBucketName, argv.meme);
                  console.log(url)
                  msg.channel.send({files: [url]})
                } catch (e) {
                  console.error(e)
                  msg.channel.send("⚠Looks like there was an error getting your meme :( check the name and try again⚠")
                }
                

            } else if (argv.signed_url) {
                // Get meme from URL.
                msg.channel.send("Getting meme .......")
                try {
                  await msg.channel.send({files: [argv.signed_url]})
                } catch (e) {
                  console.error(e)
                  msg.channel.send("⚠Looks like there was an error getting your meme URL :( check the name and try again⚠")
                }
            }


        }

        // SIGN MEME
        if (argv.subcommand_name === "sign") {
          if (!argv.meme) {
            // Print usage
            msg.channel.send(Parser.signCmd.formatHelp())
            return;
          }

            msg.channel.send("Signing meme ...");
            try {
              const url = await Bucket.generateSignedURL(memeBucketName, argv.meme);
              msg.channel.send(`"${url}"`);
            } catch(e) {
              console.error(e)
              msg.channel.send("⚠Looks like there was an error signing your meme :( check the name and try again⚠")

            }

        }
        
    } else {
      msg.channel.send(parser.formatHelp())
    }

});

main();