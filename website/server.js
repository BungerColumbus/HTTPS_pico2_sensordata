//Runs instantly as I change it because of devstart
const express = require("express");
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.static("public"));
app.use(
  "/css-reset",
  express.static(__dirname + "/node_modules/the-new-css-reset/css"),
);
app.set("view engine", "ejs");

app.get("/", (req, res) => {
  console.log("Here");
  res.render("index");
});

const testRouter = require("./routes/test");

app.use("/test", testRouter);

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
