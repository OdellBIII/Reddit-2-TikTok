// Imports necessary for web server
const express = require('express');
const app = express();
const port = 3000;

// Imports necessary for database interactions
const {MongoClient} = require('mongodb');

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

app.get('/', (req, res) => {

  res.send("Hello World!");
});

app.listen(port, () => {

  console.log(`Reddit-2-Tiktok listening at http://localhost:${port}`);
});

main().catch(console.error);
