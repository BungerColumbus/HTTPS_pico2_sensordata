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

let dataFromPico = "No data from pico yet";

app.post("/api/data", (req, res) => {
  if (req.body && req.body.status) {
    latestPicoData = req.body.status; // Update the variable
    console.log(`Received from Pico: ${latestPicoData}`);
    return res.status(200).json({ message: "Data received successfully!" });
  }
  return res.status(400).json({ error: "Oops" });
});

app.get("/", (req, res) => {
  console.log("Here");
  res.render("index", { data: dataFromPico });
});

const testRouter = require("./routes/test");

app.use("/test", testRouter);

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
