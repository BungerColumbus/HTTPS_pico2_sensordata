//Runs instantly as I change it because of devstart
const express = require("express");
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.static("public"));
app.use(
  "/css-reset",
  express.static(__dirname + "/node_modules/the-new-css-reset/css"),
);
app.use(express.json());
app.use(express.text({ type: "*/*" }));
app.set("view engine", "ejs");

let dataFromPico = "No data from pico yet";

app.post("/api/data", (req, res) => {
  console.log("Raw Body: " + req.body);

  if (typeof req.body == "string") {
    try {
      body = JSON.parse(body);
    } catch (e) {
      console.error("Failed to parse body string:", e);
    }
  }

  if (req.body && req.body.status) {
    latestPicoData = req.body.status; // Update the variable
    console.log(`Received from Pico: ${latestPicoData}`);
    return res.status(200).json({ message: "Data received successfully!" });
  }
  return res
    .status(400)
    .json({ error: "Oops, this could be invalid data format" });
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
