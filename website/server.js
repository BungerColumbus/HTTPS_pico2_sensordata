//Runs instantly as I change it because of devstart
const express = require("express");
const app = express();

app.get("/", (req, res) => {
  console.log("Here");
  res.send("Hi");
});

app.listen(3000);
