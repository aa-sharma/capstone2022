const { Server } = require("socket.io");

const io = new Server({
  // options
});

io.on("connection", (socket) => {
  io.on("message");
});

module.exports = io;
