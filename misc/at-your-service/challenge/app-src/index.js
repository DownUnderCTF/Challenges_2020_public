
'use strict';

// [START gae_node_request_example]
const express = require('express');
const path = require('path')
const bodyParser = require('body-parser')



const app = express();

app.use(bodyParser.urlencoded({ extended: false }))


app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname+'/static/index.html'))

})

app.post('/', async (req, res) => {
  await new Promise(resolve => setTimeout(resolve, 2000));
 
  if (!req.body.password) {
    return res.status(400).send('missing password')
  }

  if (req.body.password === "https://www.youtube.com/watch?v=lnigc08J6FI") {
    res.status(200).send(process.env.FLAG)
  } else {
    res.status(401).send('Bad password')
  }
});

// Start the server
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`App listening on port ${PORT}`);
  console.log('Press Ctrl+C to quit.');
});
// [END gae_node_request_example]

module.exports = app;