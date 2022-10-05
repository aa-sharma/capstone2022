const express = require("express");
const connectDB = require("./src/config/db");
const http = require("http");
const path = require("path");
const io = require("./src/websockets/ws-server");
const logger = require("./src/utils/logger");

const app = express();
const server = http.createServer(app);

// Connect DB
connectDB();

// Init middleware
app.use(express.json({ extended: false }));

app.get("/", (req, res) => res.json({ msg: "Welcome to the Apollo API..." }));

app.use("/api/users", require("./src/routes/users"));
app.use("/api/auth", require("./src/routes/auth"));

if (process.env.NODE_ENV === "production") {
  // app.use(express.static("client/build"));
  // app.get("*", (req, res) =>
  //   res.sendFile(path.resolve(__dirname, "client", "build", "index.html"))
  // );
}

const PORT = process.env.SERVER_PORT || 5000;

io.listen(server);
server.listen(PORT, () => logger.info(`Server started on port ${PORT}`));
