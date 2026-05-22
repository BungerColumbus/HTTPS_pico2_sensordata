const http = require("http");
const fs = require("fs");
const port = 3000;

const server = http.createServer(function (req, res) {
  res.writeHead(200, { "Content-Type": "text/html" });
  fs.readFile("index.html", function (error, data) {
    if (error) {
      res.writeHead(400);
      res.write("Oopsie smooopsie");
    } else {
      res.write(data);
    }
  });
});

server.listen(port, function (error) {
  if (error) {
    console.log("Uh oh... something smells poopy", error);
  } else {
    console.log("Starring weirdly at port: " + port);
  }
});
