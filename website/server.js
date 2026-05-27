// Runs instantly as I change it because of devstart
// In order to bring the updates you have made to the server do:
/*
 * push your changes to git
 * after that on the terminal of the server:
 * git pull
 * pm2 reload all
 */

// adding the const variables for express.js such as app, PORT
const express = require("express");
const app = express();
const PORT = process.env.PORT || 3000;

// showing the app what we use
app.use(express.static("public"));
app.use(
  "/css-reset",
  express.static(__dirname + "/node_modules/the-new-css-reset/css"),
);
app.use(express.json());
app.use(express.text({ type: "*/*" }));
app.set("view engine", "ejs");

// dataFromPico dynamic variable
let dataFromPico = "No data from pico yet";

// When we have a post request for our /api/data:
app.post("/api/data", (req, res) => {
  // Unpack the compressed keys from the Pico payload
  const { t1, h1, v, d } = req.body;

  // We check the body of the request and make sure it's a string
  if (typeof req.body == "string") {
    try {
      body = JSON.parse(body);
    } catch (e) {
      console.error("Failed to parse body string:", e);
    }
  }

  // We get the body of the request and its status and
  if (req.body && req.body.status) {
    dataFromPico = req.body.status; // Update the dynamic variable
    console.log(`--- New Batch Received ---`);
    console.log("Raw Body: " + req.body);
    console.log(`Room Temp: ${t1}°C`);
    console.log(`Humidity: ${h1}%`);
    console.log(`Battery Voltage: ${v}V`);
    console.log(`Distance Sensor: ${d}cm`);
    return res.status(200).json({ message: "Data received successfully!" });
  }
  // Error
  return res
    .status(400)
    .json({ error: "Oops, this could be invalid data format" });
});

// This is basically loading the index.ejs (html) on the website and also the dataFromPico on wherever I have data inserted
app.get("/", (req, res) => {
  console.log("Here");
  res.render("index", { data: dataFromPico });
});

// This is in order to connect to use the other .js files from /routes
const testRouter = require("./routes/test");

// This tells it to use the test.js file from routes.
// This is just a test to see how using different routes works (for my curiosity)
app.use("/test", testRouter);

// Listen for connections.
// A node http.Server is returned, with this application (which is a Function) as its callback.
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
