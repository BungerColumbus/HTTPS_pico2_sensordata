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
const fs = require("fs");
const path = require("path");
const app = express();
const PORT = process.env.PORT || 3000;

// showing the app what we use
const audioDirectory = path.join(__dirname, "public", "audio");
if (!fs.existsSync(audioDirectory)) {
  fs.mkdirSync(audioDirectory, { recursive: true });
}

app.use(express.static("public")); // This makes anything in 'public' downloadable!
app.use(
  "/css-reset",
  express.static(__dirname + "/node_modules/the-new-css-reset/css"),
);

app.use(express.json()); // Parses JSON payloads
// REMOVED app.use(express.text({ type: "*/*" })) to prevent binary corruption
app.set("view engine", "ejs");

// --- JSON Data Route (Unchanged) ---
let dataFromPico = { t1: 0, h1: 0, d: 0 }; // Added 'v' to match your console logs

app.post("/api/data", (req, res) => {
  const { t1, h1, d, v } = req.body;

  if (t1 !== undefined && h1 !== undefined && d !== undefined) {
    dataFromPico = { t1, h1, d };
    console.log(`--- New Batch Received ---`);
    console.log(`Room Temp: ${t1}°C`);
    console.log(`Humidity: ${h1}%`);
    console.log(`Distance: ${d}%`);
    return res.status(200).json({ message: "Data received successfully!" });
  }

  return res.status(400).json({ error: "Invalid data format" });
});

// We use express.raw() to explicitly accept binary data formatted as audio/wav
app.post(
  "/api/upload-audio",
  express.raw({ type: "audio/wav", limit: "10mb" }),
  (req, res) => {
    // Check if we actually received a buffer (binary data)
    if (!req.body || !Buffer.isBuffer(req.body)) {
      console.error("Invalid or missing audio payload.");
      return res
        .status(400)
        .json({ error: "Expected raw audio/wav binary data." });
    }

    // Define where to save the file (overwrites the previous recording)
    const filePath = path.join(audioDirectory, "latest_recording.wav");

    // Write the binary buffer directly to the disk
    fs.writeFile(filePath, req.body, (err) => {
      if (err) {
        console.error("Failed to save the WAV file:", err);
        return res
          .status(500)
          .json({ error: "Failed to save file on server." });
      }

      console.log(
        `Audio saved successfully to ${filePath} (${req.body.length} bytes)`,
      );
      res.status(200).json({ message: "Audio file received and saved." });
    });
  },
);

// View Route
app.get("/", (req, res) => {
  res.render("index", {
    distance: dataFromPico.d,
    temperature: dataFromPico.t1,
    humidity: dataFromPico.h1,
  });
});

const testRouter = require("./routes/test");
app.use("/test", testRouter);

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
