const express = require('express');
const path = require('path');
const app = express();
const port = process.env.PORT || 3000;

app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
  res.send(`<html><head><meta charset="utf-8"><title>Node.js App</title></head><body><h1>Node.js App - ${process.env.APP_VERSION || 'dev'}</h1><p>Déployé via Docker Swarm ok ça marche top</p></body></html>`);
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
