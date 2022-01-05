// Imports necessary for web server
import express from 'express';
const app = express();
const port = process.env.port || 3000;
import bodyParser from 'body-parser';

app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());

// Imports necessary for database interactions
import {MongoClient} from 'mongodb';

// Used for calling Reddit API
import fetch from 'node-fetch';
// Testing whether MongoDB works

async function listDatabases(client){
  databasesList = await client.db().admin().listDatabases();

  console.log("Databases:");
  databasesList.databases.forEach(db => console.log(` - ${db.name}`));
}

async function main(){

  const uri = 'mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000';
  const client = new MongoClient(uri);
  try {
    await client.connect();
    await listDatabases(client);
  } catch(e) {
    console.error(e);
  } finally {
    await client.close();
  }
}

// Dummy endpoint that we can modify later
app.get('/', (req, res) => {

  res.send("Hello World!");
});

// Basic endpoint for getting the most popular post from a subreddit with Title and Body text
app.get('/subreddit/:subredditName', (req, res) => {

  fetch(`https://www.reddit.com/r/${req.params.subredditName}/hot.json`)
  .then(result => result.json())
  .then(data => data['data']['children'][2])
  .then(postObject => {
    const postResponse = {
      title : postObject['data']['title'],
      body : postObject['data']['selftext_html'],
      url: postObject['data']['url']
    }

    console.log(postResponse);
    res.send(postResponse);
  })
  .catch(error => console.error(error));
});

app.listen(port, () => {

  console.log(`Reddit-2-Tiktok listening at http://localhost:${port}`);
});

//main().catch(console.error);
