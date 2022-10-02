const { Server } = require("socket.io");

const io = new Server({
  // options
});

io.on("connection", (socket) => {
  // ...
});

module.exports = io;
