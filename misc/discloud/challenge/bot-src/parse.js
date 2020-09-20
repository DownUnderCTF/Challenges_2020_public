const ArgumentParser = require('argparse').ArgumentParser;

const parser = new ArgumentParser({
    description: 'Getcha memes, get em fast get em quick 😂😂😂',
    prog: '!meme',
    addHelp: false
});

const subparsers = parser.addSubparsers({
    title:'subcommands',
    dest:"subcommand_name"
});

const listCmd = subparsers.addParser('list', 
{
  addHelp:true,
  help: "You don't know the memes, boy do I have the command for you"
});



const getCmd = subparsers.addParser(
  'get',
  {
    addHelp: false,
    help: "Gives you memes. Now. ‼"
  }
);

getCmd.addArgument(
  [ '-m', '--meme' ],
  {
    required: false,
    help: "The name of the meme you wannna get 😂😂"
  }
);

getCmd.addArgument(
    [ '-su', '--signed-url' ],
    {
      required: false,
      help: "Someone sent you a GCS signed URL of a meme? Put it here and I'll get it for you and your friends 😎"
    }
  );

  const signCmd = subparsers.addParser(
    'sign',
    {
      addHelp: false,
      help: "Now send memes to your friends! 😘😘"
    }
  );
  
  signCmd.addArgument(
    ['-m', '--meme'],
    {
      help: "Name of the meme you wanna send ya friend :D 😘 | not actually optional",
      required: false
    }
  );


  ArgumentParser.prototype.error = function (err) {
    var message;
    if (err instanceof Error) {
      if (this.debug === true) {
        throw err;
      }
      message = err.message;
    } else {
      message = err;
    }
  
    if (this.debug === true) {
      throw new Error(msg);
    }
  
    throw "Invalid command \n" + this.formatHelp();
  };

  exports.parser = parser;
  exports.getCmd = getCmd;
  exports.listCmd = listCmd;
  exports.signCmd = signCmd;