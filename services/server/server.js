const express = require("express");
const connectDB = require("./config/db");
const http = require("http");
const path = require("path");
const io = require("./websockets/ws-server");

const app = express();
const server = http.createServer(app);

// Connect DB
connectDB();

// Init middleware
app.use(express.json({ extended: false }));

app.get("/", (req, res) => res.json({ msg: "Welcome to the Apollo API..." }));

app.use("/api/users", require("./routes/users"));
app.use("/api/auth", require("./routes/auth"));

if (process.env.NODE_ENV === "prod") {
  // app.use(express.static("client/build"));
  // app.get("*", (req, res) =>
  //   res.sendFile(path.resolve(__dirname, "client", "build", "index.html"))
  // );
}

const PORT = process.env.PORT || 5000;

io.listen(server);
server.listen(PORT, () => console.log(`Server started on port ${PORT}`));
